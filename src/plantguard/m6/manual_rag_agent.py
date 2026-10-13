
from functools import lru_cache
from pathlib import Path

from src.plantguard.m4.service import PlantGuardRetrievalService
from src.plantguard.m6.permissions import scoped


PROJECT_ROOT = Path(__file__).resolve().parents[3]


@lru_cache(maxsize=1)
def get_retrieval_service():
    """Reuse one retrieval pipeline rather than reinitializing it per event."""
    return PlantGuardRetrievalService(
        corpus_path=str(PROJECT_ROOT / "data/plantguard/corpus"),
        candidate_limit=10,
        final_limit=5,
    )


@scoped("manual_rag")
def manual_rag_agent(state: dict) -> dict:
    """Retrieve relevant manual/SOP passages for a maintenance event."""
    event = state.get("event")

    if not isinstance(event, dict):
        return {
            "error": "Manual RAG requires a valid maintenance event.",
            "audit_log": ["manual_rag: missing maintenance event"],
        }

    question = (
        f"Asset: {event.get('asset_tag', 'unknown')}\n"
        f"Maintenance issue: {event.get('raw_text', '')}\n"
        f"Sensor readings: {event.get('readings', {})}\n"
        "Find relevant maintenance procedures, diagnostic guidance, "
        "safety precautions, and evidence gaps. Do not infer that "
        "a procedure is safe solely because it appears in a manual."
    )

    try:
        results = get_retrieval_service().retrieve(question)

        passages = []

        for item in results:
            if not isinstance(item, dict):
                continue

            # Unwrap the M4 retrieval/reranking result.
            current = item

            for _ in range(3):
                if not isinstance(current, dict):
                    break

                if isinstance(current.get("chunk"), dict):
                    current = current["chunk"]
                    break

                nested = current.get("result")
                if not isinstance(nested, dict):
                    break

                current = nested

            if not isinstance(current, dict):
                continue

            text = current.get("text") or current.get("page_content")
            metadata = current.get("metadata") or {}

            if not isinstance(text, str) or not text.strip():
                continue

            if not isinstance(metadata, dict):
                metadata = {}

            passages.append({
                "source": metadata.get("source", "unknown"),
                "section": metadata.get("section", ""),
                "text": text,
            })

        if not passages:
            return {
                "findings": [{
                    "agent": "manual_rag",
                    "status": "insufficient_evidence",
                    "passages": [],
                }],
                "audit_log": [
                    "manual_rag: no usable manual passages retrieved"
                ],
            }

        return {
            "findings": [{
                "agent": "manual_rag",
                "status": "success",
                "passages": passages,
            }],
            "audit_log": [
                f"manual_rag: retrieved {len(passages)} manual passages"
            ],
        }

    except Exception as exc:
        return {
            "findings": [{
                "agent": "manual_rag",
                "status": "error",
                "passages": [],
                "error": str(exc),
            }],
            "audit_log": ["manual_rag: retrieval failed"],
        }
