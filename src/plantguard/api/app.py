import os
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="PlantGuard API",
    description="Predictive Maintenance & Supply Chain Ops Copilot",
    version="1.0.0",
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_ROOT = PROJECT_ROOT / "data/plantguard"


class AnalyzeRequest(BaseModel):
    asset_tag: str = Field(..., min_length=1, max_length=100)
    raw_text: str = Field(..., min_length=1)
    event_id: str = Field(default="API-REQUEST")
    readings: dict = Field(default_factory=dict)


def _llm_configured() -> bool:
    return bool(
        os.environ.get("PLANTGUARD_LLM_API_KEY")
        or os.environ.get("GROQ_API_KEY")
    )


def _classify_route(result: dict) -> str:
    recommendation = result.get("recommendation") or {}
    refusal = (
        recommendation.get("refusal", {})
        if isinstance(recommendation, dict)
        else {}
    )
    if bool(result.get("__interrupt__")):
        return "human_review"
    if refusal.get("refused") is True and result.get("status") == "refused":
        return "refuse"
    if bool(result.get("approval_required")):
        return "human_review"
    return "auto"


def _extract_answer(result: dict) -> str:
    recommendation = result.get("recommendation") or {}
    if isinstance(recommendation, dict):
        return recommendation.get("summary", "")
    return str(recommendation or "")


def _extract_citations(result: dict) -> list[str]:
    citations = []
    recommendation = result.get("recommendation") or {}
    if isinstance(recommendation, dict):
        citations.extend(
            item.get("source", "")
            for item in recommendation.get("evidence", [])
            if isinstance(item, dict) and item.get("source")
        )
    for finding in result.get("findings", []):
        if finding.get("agent") == "manual_rag":
            citations.extend(
                item.get("source", "")
                for item in finding.get("passages", [])
                if item.get("source")
            )
    return sorted(set(filter(None, citations)))


@app.get("/health")
def health():
    """Basic API liveness check."""
    return {
        "status": "healthy",
        "service": "PlantGuard",
    }


@app.get("/status")
def status():
    """Report live configuration and dependency readiness."""
    data_assets = {
        "corpus_index": (DATA_ROOT / "corpus/index.json").exists(),
        "intake_records": (DATA_ROOT / "intake/records.jsonl").exists(),
        "mock_api_tables": (DATA_ROOT / "mock_api/assets.json").exists(),
        "golden_set": (DATA_ROOT / "eval/golden_set.json").exists(),
        "manifest": (DATA_ROOT / "manifest.json").exists(),
    }
    dependencies = {
        "llm_api_key": "configured" if _llm_configured() else "missing",
        "qdrant": (
            "configured" if os.environ.get("QDRANT_URL") else "not_configured"
        ),
        "embeddings_api_key": (
            "configured" if os.environ.get("GOOGLE_API_KEY") else "missing"
        ),
        "langfuse": (
            "configured"
            if os.environ.get("LANGFUSE_PUBLIC_KEY")
            else "not_configured"
        ),
    }
    ready = _llm_configured() and all(data_assets.values())

    return {
        "service": "PlantGuard",
        "status": "operational",
        "ready": ready,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "components": {
            "log_intake": "configured",
            "manual_sop_rag": "configured",
            "maintenance_recommendation": "configured",
            "safety_reviewer": "configured",
            "human_approval": "configured",
            "procurement": "simulated_only",
            "langfuse_cloud_tracing": "unverified",
        },
        "dependencies": dependencies,
        "data_assets": data_assets,
        "safety": {
            "automatic_maintenance_execution": False,
            "human_review_for_flagged_cases": True,
        },
    }


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    """Run the maintenance agent team on a single maintenance event."""
    if not _llm_configured():
        return {
            "status": "unavailable",
            "message": (
                "LLM is not configured. Set GROQ_API_KEY or "
                "PLANTGUARD_LLM_API_KEY to enable analysis."
            ),
            "execution_authorized": False,
        }

    from src.plantguard.m6.graph import build_graph

    graph = build_graph()

    try:
        result = graph.invoke(
            {
                "event": {
                    "event_id": request.event_id,
                    "asset_tag": request.asset_tag,
                    "raw_text": request.raw_text,
                    "readings": request.readings,
                }
            },
            config={
                "configurable": {"thread_id": f"api-{request.event_id}"},
                "recursion_limit": 30,
            },
        )
    except Exception as exc:
        return {
            "status": "error",
            "message": f"Analysis failed: {type(exc).__name__}",
            "execution_authorized": False,
        }

    route = _classify_route(result)

    return {
        "status": result.get(
            "status", "interrupted" if route == "human_review" else "completed"
        ),
        "route": route,
        "answer": _extract_answer(result),
        "citations": _extract_citations(result),
        "approval_required": bool(result.get("approval_required")),
        "interrupted": bool(result.get("__interrupt__")),
        "safety_review": result.get("safety_review"),
        "procurement_result": result.get("procurement_result"),
        "execution_authorized": False,
    }
