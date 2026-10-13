import asyncio
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt

from src.plantguard.m6.intake_agent import intake_agent
from src.plantguard.m6.maintenance_agent import maintenance_agent
from src.plantguard.m6.procurement_agent import procurement_agent
from src.plantguard.m6.researcher_agent import researcher_agent
from src.plantguard.m6.safety_reviewer_agent import safety_reviewer_agent
from src.plantguard.m6.state import PlantGuardTeamState
from src.plantguard.m6.recommendation_reviewer_agent import (
    recommendation_reviewer_agent,
)
from src.plantguard.m6.manual_rag_agent import manual_rag_agent
from src.plantguard.observability.tracing import traced_node
MAX_REVISIONS = 2


def initialize_revision_state(state: dict) -> dict:
    return {
        "revision_count": state.get("revision_count", 0),
    }

def route_after_recommendation(state: dict) -> str:
    """Route reviewed recommendations, allowing at most two revisions."""
    if state.get("error"):
        return "safety_reviewer"

    review = state.get("recommendation_review") or {}

    if review.get("passed") is True:
        return "procurement" if state.get("part_number") else "safety_reviewer"

    revision_count = state.get("revision_count", 0)

    if revision_count < MAX_REVISIONS:
        return "revise_recommendation"

    return "safety_reviewer"


def revise_recommendation_node(state: dict) -> dict:
    """Record a bounded revision attempt and invalidate the prior review."""
    revision_count = state.get("revision_count", 0) + 1
    review = state.get("recommendation_review") or {}
    issues = review.get("issues", [])

    print("REVISION TRIGGERED — previous review issues:", issues)
    return {
        "revision_count": revision_count,
        "revision_feedback": issues,
        "recommendation_review": {
            "status": "pending",
            "passed": False,
            "issues": issues,
            "execution_authorized": False,
        },
        "audit_log": [
            f"supervisor: recommendation revision attempt "
            f"{revision_count}/{MAX_REVISIONS}"
        ],
    }

def route_after_safety_review(state: dict) -> str:
    if state.get("approval_required"):
        return "human_review"
    return "finish"


def human_review_node(state: dict) -> dict:
    """Pause execution until a human explicitly approves or rejects."""
    decision = interrupt({
        "type": "maintenance_approval",
        "event_id": (state.get("event") or {}).get("event_id"),
        "asset_tag": (state.get("event") or {}).get("asset_tag"),
        "recommendation": state.get("recommendation"),
        "safety_review": state.get("safety_review"),
        "message": "Review this maintenance case and approve or reject it.",
    })

    if not isinstance(decision, dict):
        return {
            "approval_status": "rejected",
            "status": "rejected",
            "audit_log": ["supervisor: invalid approval response; rejected"],
        }

    approved = decision.get("approved") is True

    return {
        "approval_status": "approved" if approved else "rejected",
        "status": "approved_for_human_supervised_next_step"
        if approved else "rejected",
        "audit_log": [
            "supervisor: human approved case; no maintenance action executed"
            if approved else
            "supervisor: human rejected case; no maintenance action executed"
        ],
    }


def finish_node(state: dict) -> dict:
    return {
        "status": "completed",
        "approval_status": "not_required",
        "audit_log": [
            "supervisor: workflow completed; no maintenance action executed"
        ],
    }

def researcher_sync(state: dict) -> dict:
    return asyncio.run(researcher_agent(state))


def procurement_sync(state: dict) -> dict:
    return asyncio.run(procurement_agent(state))

def build_graph(checkpointer=None):
    builder = StateGraph(PlantGuardTeamState)

    builder.add_node("intake", traced_node("intake", intake_agent))
    builder.add_node(
        "recommendation",
        traced_node("recommendation", maintenance_agent),
    )
    builder.add_node(
        "safety_reviewer",
        traced_node("safety_reviewer", safety_reviewer_agent),
    )
    builder.add_node(
        "researcher",
        traced_node("researcher", researcher_sync),
    )
    builder.add_node(
        "manual_rag",
        traced_node("manual_rag", manual_rag_agent),
    )
    builder.add_node(
        "recommendation_reviewer",
        traced_node("recommendation_reviewer", recommendation_reviewer_agent),
    )
    builder.add_node(
        "revise_recommendation",
        traced_node("revise_recommendation", revise_recommendation_node),
    )
    builder.add_node(
        "initialize_revision_state",
        traced_node("initialize_revision_state", initialize_revision_state),
    )
    builder.add_node("finish", traced_node("finish", finish_node))
    builder.add_node("human_review", human_review_node)
    builder.add_node("procurement", procurement_sync)


    builder.add_edge(START, "intake")
    builder.add_edge("intake", "initialize_revision_state")
    builder.add_edge("initialize_revision_state", "researcher")
    builder.add_edge("researcher", "manual_rag")
    builder.add_edge("manual_rag", "recommendation")
    builder.add_edge("recommendation", "recommendation_reviewer")


    builder.add_conditional_edges(
        "recommendation_reviewer",
        route_after_recommendation,
        {
            "procurement": "procurement",
            "safety_reviewer": "safety_reviewer",
            "revise_recommendation": "revise_recommendation"
        },
    )
    builder.add_edge("revise_recommendation", "recommendation")
    builder.add_edge("procurement", "safety_reviewer")

    builder.add_conditional_edges(
        "safety_reviewer",
        route_after_safety_review,
        {
            "human_review": "human_review",
            "finish": "finish",
        },
    )

    builder.add_edge("human_review", END)
    builder.add_edge("finish", END)

    return builder.compile(checkpointer=checkpointer or MemorySaver())
