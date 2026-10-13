import pytest

from src.plantguard.m6.graph import build_graph
from src.plantguard.m6.graph import route_after_recommendation
from langgraph.types import Command

def test_graph_routes_safety_critical_event_to_human_review():
    graph = build_graph()
    result = graph.invoke(
        {
            "event": {
                "event_id": "EVT-2001",
                "source": "sensor",
                "asset_code": "CNC-MILL",
                "asset_tag": "VPW-CNC-MILL-03",
                "raw_text": "High voltage electrical maintenance required",
                "readings": {"vibration_mm_s": 12.5},
            },
        },
        config={"configurable": {"thread_id": "test-event-2001"}},
    )

    assert result.get("__interrupt__")
    assert result["approval_required"] is True
    assert result["safety_review"]["execution_authorized"] is False

def test_graph_can_skip_procurement_without_part_number():
    graph = build_graph()

    result = graph.invoke(
        {
            "event": {
                "event_id": "EVT-2002",
                "source": "sensor",
                "asset_code": "CNC-MILL",
                "asset_tag": "VPW-CNC-MILL-03",
                "raw_text": "Vibration alert",
                "readings": {"vibration_mm_s": 2.2},
            },
        },
        config={"configurable": {"thread_id": "test-event-2002"}},
    )

    assert result["status"] == "completed"
    assert result.get("error") is None
    assert result["approval_required"] is False
    assert result["safety_review"]["execution_authorized"] is False
    assert result.get("procurement_result") is None
    assert result["recommendation_review"]["passed"] is True
    assert result["revision_count"] <=2


def test_failed_review_requests_revision_before_limit():
    state = {
        "recommendation_review": {
            "passed": False,
            "issues": ["Evidence source is missing."],
        },
        "revision_count": 0,
    }

    assert route_after_recommendation(state) == "revise_recommendation"


def test_failed_review_can_retry_once_more():
    state = {
        "recommendation_review": {
            "passed": False,
            "issues": ["Evidence source is missing."],
        },
        "revision_count": 1,
    }

    assert route_after_recommendation(state) == "revise_recommendation"


def test_failed_review_escalates_after_two_revisions():
    state = {
        "recommendation_review": {
            "passed": False,
            "issues": ["Evidence source is missing."],
        },
        "revision_count": 2,
    }

    assert route_after_recommendation(state) == "safety_reviewer"


def test_passed_review_routes_to_safety_without_part_number():
    state = {
        "recommendation_review": {"passed": True},
        "revision_count": 0,
    }

    assert route_after_recommendation(state) == "safety_reviewer"


def test_passed_review_routes_to_procurement_when_part_requested():
    state = {
        "recommendation_review": {"passed": True},
        "part_number": "FILTER-001",
        "revision_count": 0,
    }

    assert route_after_recommendation(state) == "procurement"




def test_rejected_safety_critical_event_stops_without_action():
    graph = build_graph()
    config = {"configurable": {"thread_id": "test-rejected-event-2003"}}

    result = graph.invoke(
        {
            "event": {
                "event_id": "EVT-2003",
                "source": "sensor",
                "asset_code": "CNC-MILL",
                "asset_tag": "VPW-CNC-MILL-03",
                "raw_text": "High voltage electrical maintenance required",
                "readings": {"vibration_mm_s": 12.5},
            },
        },
        config=config,
    )

    assert result.get("__interrupt__")

    result = graph.invoke(
        Command(resume={"approved": False}),
        config=config,
    )

    assert result["approval_status"] == "rejected"
    assert result["status"] == "rejected"
    assert result.get("procurement_result") is None
    assert any(
        "no maintenance action executed" in entry
        for entry in result["audit_log"]
    )
