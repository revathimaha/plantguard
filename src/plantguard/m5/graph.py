from langgraph.graph import StateGraph, START, END

from src.plantguard.m5.state import PlantGuardState
from src.plantguard.m5.nodes import (
    intake_node,
    root_cause_lookup_node,
    recommendation_node,
    safety_routing_node,
    human_approval_node
)



def route_after_safety(state: PlantGuardState) -> str:
    """Pure routing function: decide which path to take."""
    if state.get("route") == "human_approval":
        return "human_approval"

    return "auto_log"


def auto_log_node(state: PlantGuardState) -> dict:
    """Record a non-safety-critical maintenance event."""
    return {
        "status": "auto_logged",
        "audit_log": [
            "Maintenance event automatically logged."
        ],
    }

def route_after_human(state: PlantGuardState) -> str:
    """Route based on the human's decision."""

    if state.get("approval_status") == "approved":
        return "approved"

    return "rejected"

def approval_complete_node(state: PlantGuardState) -> dict:
    """Record that a safety-critical action was approved."""

    return {
        "status": "approved_for_execution",
        "audit_log": [
            "Safety-critical recommendation approved by human."
        ],
    }

def rejection_node(state: PlantGuardState) -> dict:
    """Record that the safety-critical recommendation was rejected."""

    return {
        "status": "rejected",
        "audit_log": [
            "Safety-critical recommendation rejected by human."
        ],
    }


def build_graph():
    graph = StateGraph(PlantGuardState)

    # Nodes
    graph.add_node("intake", intake_node)
    graph.add_node("root_cause_lookup", root_cause_lookup_node)
    graph.add_node("recommendation", recommendation_node)
    graph.add_node("safety_routing", safety_routing_node)
    graph.add_node("auto_log", auto_log_node)
    graph.add_node("human_approval", human_approval_node)
    graph.add_node("approval_complete",approval_complete_node)
    graph.add_node("rejection",rejection_node)

    # Linear workflow
    graph.add_edge(START, "intake")
    graph.add_edge("intake", "root_cause_lookup")
    graph.add_edge("root_cause_lookup", "recommendation")
    graph.add_edge("recommendation", "safety_routing")

    # Conditional safety routing
    graph.add_conditional_edges(
        "safety_routing",
        route_after_safety,
        {
            "auto_log": "auto_log",
            "human_approval": "human_approval",
        },
    )

    graph.add_conditional_edges(
        "human_approval",
        route_after_human,
        {
            "approved": "approval_complete",
            "rejected": "rejection",
        },
    )

    graph.add_edge("auto_log", END)
    graph.add_edge("approval_complete", END)
    graph.add_edge("rejection", END)

    graph.add_edge("auto_log", END)

    return graph