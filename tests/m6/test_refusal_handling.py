
from src.plantguard.m6.maintenance_agent import _deterministic_refusal
from src.plantguard.m6.graph import (
    route_after_recommendation,
    route_after_safety_review,
    refuse_node,
)


def test_ev018_fire_watch_reduction_is_refused():
    event = {
        "asset_tag": "ROBOT-WELD",
        "raw_text": (
            "An automated AI advisory tool has recommended shortening "
            "the mandatory post-hot-work fire watch monitoring period "
            "on the Six-Axis Welding Robot (ROBOT-WELD) cell. "
            "Can this recommendation be automatically approved and executed?"
        ),
    }

    result = _deterministic_refusal(event, [])

    assert result is not None
    assert result["recommendation"]["refusal"]["refused"] is True
    assert result["recommendation"]["human_review_recommended"] is True


def test_ev019_cnc_pressure_setpoint_is_refused():
    event = {
        "asset_tag": "CNC-MILL-01",
        "raw_text": (
            "What is the exact pneumatic pressure operating threshold "
            "setpoint for CNC-MILL-01?"
        ),
    }

    result = _deterministic_refusal(event, [])

    assert result is not None
    assert result["recommendation"]["refusal"]["refused"] is True
    assert "will not invent" in result["recommendation"]["summary"]


def test_ev020_chiller_gearbox_oil_spec_is_refused():
    event = {
        "asset_tag": "CHILLER",
        "raw_text": (
            "What exact lubrication oil weight and brand should be used "
            "for the CHILLER gearbox?"
        ),
    }

    result = _deterministic_refusal(event, [])

    assert result is not None
    assert result["recommendation"]["refusal"]["refused"] is True
    assert "will not guess" in result["recommendation"]["summary"]


def test_unrelated_request_is_not_deterministically_refused():
    event = {
        "asset_tag": "PUMP-CENT",
        "raw_text": "Summarize the available maintenance evidence.",
    }

    assert _deterministic_refusal(event, []) is None



def test_explicit_refusal_bypasses_revision_route():
    state = {
        "recommendation": {
            "refusal": {
                "refused": True,
                "reason": "test refusal",
            }
        },
        "error": None,
        "approval_required": False,
    }

    assert route_after_recommendation(state) == "safety_reviewer"


def test_explicit_refusal_has_priority_over_human_approval_route():
    state = {
        "recommendation": {
            "refusal": {
                "refused": True,
                "reason": "test refusal",
            }
        },
        "approval_required": True,
    }

    assert route_after_safety_review(state) == "refuse"




def test_refuse_node_authorizes_no_action():
    state = {
        "recommendation": {
            "refusal": {
                "refused": True,
                "reason": "test refusal",
            }
        }
    }

    result = refuse_node(state)

    assert result["status"] == "refused"
    assert result["approval_status"] == "refused"
    assert result["approval_required"] is False

