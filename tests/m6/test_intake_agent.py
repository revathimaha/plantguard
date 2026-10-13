from src.plantguard.m6.intake_agent import intake_agent


def test_intake_agent_accepts_valid_event():
    state = {
        "event": {
            "event_id": "EVT-1001",
            "asset_tag": "CNC-MILL-03",
            "raw_text": "High vibration detected",
            "readings": {"vibration_mm_s": 12.5},
        }
    }

    result = intake_agent(state)

    assert len(result["plan"]) == 4
    assert result["findings"][0]["asset_tag"] == "CNC-MILL-03"
    assert "error" not in result


def test_intake_agent_rejects_missing_event():
    result = intake_agent({})

    assert "error" in result
    assert result["audit_log"]


def test_intake_agent_cannot_change_safety_approval():
    # The intake agent's permission scope must remain enforced.
    # Its normal implementation never writes approval fields.
    result = intake_agent({
        "event": {
            "event_id": "EVT-1002",
            "asset_tag": "CNC-MILL-03",
            "raw_text": "Temperature elevated",
            "readings": {},
        }
    })

    assert "approval_required" not in result
    assert "safety_review" not in result