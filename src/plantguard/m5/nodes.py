from src.plantguard.m5.state import PlantGuardState
from langgraph.types import interrupt


def human_approval_node(state: PlantGuardState) -> dict:
    """
    Pause the workflow and request human approval
    for a safety-critical maintenance recommendation.
    """

    decision = interrupt(
        {
            "question": "Approve this safety-critical maintenance recommendation?",
            "asset_tag": state["event"].get("asset_tag", "unknown"),
            "recommendation": state.get("recommendation", ""),
            "root_cause_evidence": state.get(
                "root_cause_evidence", []
            ),
            "safety_critical": state.get("safety_critical", False),
        }
    )

    return {
        "approval_status": decision.get("action", "rejected"),
        "approver_note": decision.get("note", ""),
        "status": "approval_received",
        "audit_log": [
            f"Human approval decision received: "
            f"{decision.get('action', 'unknown')}."
        ],
    }

def intake_node(state: PlantGuardState) -> dict:
    """
    Validate that the workflow received a maintenance event.

    M1 is responsible for producing the validated MaintenanceEvent.
    M5 only orchestrates that event.
    """

    event = state.get("event")

    if not event:
        return {
            "status": "failed",
            "error": "No maintenance event provided.",
            "audit_log": ["Intake failed: no maintenance event."],
        }

    return {
        "status": "intake_complete",
        "error": "",
        "audit_log": [
            f"Alert intake completed for asset "
            f"{event.get('asset_tag', 'unknown')}."
        ],
    }

def root_cause_lookup_node(state: PlantGuardState) -> dict:
    """
    Retrieve maintenance evidence using the production M4
    BM25 + dense + hybrid RRF + cross-encoder pipeline.
    """

    from src.plantguard.m4.service import PlantGuardRetrievalService

    event = state["event"]

    asset_tag = event.get("asset_tag", "unknown")
    raw_text = event.get("raw_text", "").strip()

    if not raw_text:
        return {
            "root_cause_evidence": [],
            "status": "root_cause_lookup_failed",
            "error": "Maintenance event contains no raw_text.",
            "audit_log": [
                f"Root-cause lookup failed for {asset_tag}: "
                "no maintenance description provided."
            ],
        }

    retrieval_service = PlantGuardRetrievalService()

    reranked_results = retrieval_service.retrieve(
        question=raw_text,
    )

    if not reranked_results:
        return {
            "root_cause_evidence": [],
            "status": "root_cause_lookup_failed",
            "error": "No relevant maintenance evidence found.",
            "audit_log": [
                f"Root-cause lookup found no evidence for {asset_tag}."
            ],
        }

    evidence = []

    for index, item in enumerate(
        reranked_results,
        start=1,
    ):
        hybrid_item = item["result"]
        result = hybrid_item["result"]

        if isinstance(result, dict):
            chunk = result["chunk"]

            source = chunk["metadata"]["source"]
            section = chunk["metadata"]["section"]
            text = chunk["text"]

        else:
            source = result.payload["source"]
            section = result.payload["section"]
            text = result.payload["text"]

        evidence.append(
            {
                "id": f"E{index}",
                "asset_tag": asset_tag,
                "query": raw_text,
                "source": source,
                "section": section,
                "text": text,
                "rerank_score": item["rerank_score"],
            }
        )

    return {
        "root_cause_evidence": evidence,
        "status": "root_cause_lookup_complete",
        "error": "",
        "audit_log": [
            f"Root-cause lookup completed for {asset_tag}; "
            f"{len(evidence)} evidence items retrieved."
        ],
    }

def recommendation_node(state: PlantGuardState) -> dict:
    """
    Generate a maintenance recommendation grounded in the
    evidence retrieved by the M4 pipeline.
    """

    import os

    from src.plantguard.llm.client import LLMClient
    from src.plantguard.m4.rag import PlantGuardRAG

    event = state.get("event", {})
    evidence = state.get("root_cause_evidence", [])

    if not evidence:
        return {
            "rag_answer": "",
            "rag_sources": [],
            "recommendation": "",
            "status": "recommendation_failed",
            "error": "No root-cause evidence available.",
            "audit_log": [
                "Recommendation failed: no root-cause evidence."
            ],
        }

    # Convert the M5 evidence representation back into the
    # structure expected by the existing M4 RAG component.
    reranked_results = []

    for item in evidence:
        chunk = {
            "text": item["text"],
            "metadata": {
                "source": item["source"],
                "section": item["section"],
            },
        }

        reranked_results.append(
            {
                "result": {
                    "result": {
                        "chunk": chunk,
                    }
                },
                "rerank_score": item.get("rerank_score", 0.0),
            }
        )

    rag = PlantGuardRAG(
        llm_client=LLMClient(
            "groq/openai/gpt-oss-20b",
            api_key=os.environ["GROQ_API_KEY"],
        )
    )

    raw_text = event.get("raw_text", "").strip()

    query = (
        "For this maintenance event:\n"
        f"{raw_text}\n\n"
        "Based ONLY on the supplied PlantGuard maintenance evidence, "
        "what maintenance action or approved procedure is supported? "
        "If the evidence is insufficient to recommend a specific action, "
        "state that the evidence is insufficient. "
        "Do not invent a procedure."
    )

    rag_result = rag.answer(
        query=query,
        reranked_results=reranked_results,
    )

    recommendation = rag_result["answer"]

    return {
        "rag_answer": rag_result["answer"],
        "rag_sources": rag_result["sources"],
        "recommendation": recommendation,
        "status": "recommendation_complete",
        "error": "",
        "audit_log": [
            "Maintenance recommendation generated from M4-grounded evidence."
        ],
    }


def safety_routing_node(state: PlantGuardState) -> dict:
    """
    Deterministically classify whether the maintenance event
    requires human approval.

    The safety decision must not depend on model-generated wording.
    """

    event = state.get("event", {})
    raw_text = event.get("raw_text", "").lower()

    safety_indicators = [
        "lockout",
        "tagout",
        "electrical",
        "high voltage",
        "energized",
        "pressure",
        "hydraulic",
        "confined space",
        "hot work",
        "live circuit",
        "live electrical",
    ]

    matched_indicators = [
        keyword
        for keyword in safety_indicators
        if keyword in raw_text
    ]

    safety_critical = bool(matched_indicators)

    route = (
        "human_approval"
        if safety_critical
        else "auto_log"
    )

    classification = (
        "SAFETY-CRITICAL"
        if safety_critical
        else "MINOR"
    )

    return {
        "safety_critical": safety_critical,
        "route": route,
        "status": "safety_routing_complete",
        "audit_log": [
            f"Safety classification: {classification}; "
            f"matched_indicators={matched_indicators}; "
            f"route={route}."
        ],
    }