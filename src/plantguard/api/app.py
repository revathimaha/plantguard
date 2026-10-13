
from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="PlantGuard API",
    description="Predictive Maintenance & Supply Chain Ops Copilot",
    version="1.0.0",
)


@app.get("/health")
def health():
    """Basic API liveness check."""
    return {
        "status": "healthy",
        "service": "PlantGuard",
    }


@app.get("/status")
def status():
    """Report application capabilities without running workflow actions."""
    return {
        "service": "PlantGuard",
        "status": "operational",
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
        "safety": {
            "automatic_maintenance_execution": False,
            "human_review_for_flagged_cases": True,
        },
    }
