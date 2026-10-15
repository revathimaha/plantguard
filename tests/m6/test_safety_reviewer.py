from src.plantguard.m6.safety_reviewer_agent import (
    safety_reviewer_agent,
    is_factual_standards_question,
    is_high_risk_maintenance_request,
)

def test_implausible_conveyor_readings_require_human_review():
    state = {
        "event": {
            "event_id": "PLANTGUARD-EV-902",
            "asset_tag": "CONV-BELT-01",
            "raw_text": (
                "Conveyor belt reports vibration of 912 mm/s "
                "and temperature of -40 C. Do not suppress the alarm."
            ),
            "readings": {
                "vibration_mm_s": 912,
                "temperature_c": -40,
            },
        },
        "recommendation": {
            "summary": (
                "Readings are implausible; verify the sensors and escalate."
            )
        },
        "findings": [
            {"agent": "researcher", "status": "success"}
        ],
    }

    result = safety_reviewer_agent(state)

    assert result["approval_required"] is True
    assert result["safety_review"]["execution_authorized"] is False



def test_bypass_request_requires_human_approval():
    state = {
        "event": {
            "event_id": "TEST-BYPASS",
            "asset_tag": "HYD-PRESS-01",
            "raw_text": "Skip the paperwork and start the technician immediately.",
            "readings": {},
        },
        "recommendation": {"summary": "Proceed with maintenance."},
        "findings": [
            {"agent": "researcher", "status": "success"},
        ],
    }

    result = safety_reviewer_agent(state)

    assert result["approval_required"] is True
    assert result["safety_review"]["status"] == "human_approval_required"
    assert result["safety_review"]["execution_authorized"] is False
    assert "bypass" in result["safety_review"]["reason"].lower()


def test_ammonia_leak_without_manual_requires_review():
    state = {
        "event": {
            "event_id": "TEST-AMMONIA",
            "asset_tag": "CHILLER-01",
            "raw_text": "Ammonia leak reported near the refrigeration unit.",
            "readings": {},
        },
        "recommendation": {"summary": "Investigate the reported leak."},
        "findings": [
            {"agent": "researcher", "status": "success"},
        ],
    }

    result = safety_reviewer_agent(state)

    assert result["approval_required"] is True
    assert result["safety_review"]["status"] == "human_approval_required"
    assert result["safety_review"]["execution_authorized"] is False
    assert "ammonia" in result["safety_review"]["reason"].lower()


def test_ammonia_with_successful_manual_does_not_trigger_missing_procedure():
    state = {
        "event": {
            "event_id": "TEST-AMMONIA-MANUAL",
            "asset_tag": "CHILLER-01",
            "raw_text": "Ammonia leak reported near the refrigeration unit.",
            "readings": {},
        },
        "recommendation": {"summary": "Follow the approved procedure."},
        "findings": [
            {"agent": "researcher", "status": "success"},
            {"agent": "manual_rag", "status": "success"},
        ],
    }

    result = safety_reviewer_agent(state)

    # The missing-procedure condition alone must not trigger approval.
    assert result["safety_review"]["status"] == "review_passed"
    assert result["safety_review"]["execution_authorized"] is False


def test_recommendation_failure_requires_human_review():
    state = {
        "event": {
            "event_id": "TEST-RECOMMENDATION-FAILURE",
            "asset_tag": "CNC-MILL-03",
            "raw_text": "Vibration alert",
            "readings": {},
        },
        "recommendation": {
            "summary": "Recommendation generation failed."
        },
        "findings": [
            {"agent": "researcher", "status": "success"},
            {"agent": "maintenance", "status": "error"},
        ],
    }

    result = safety_reviewer_agent(state)

    assert result["approval_required"] is True
    assert result["safety_review"]["status"] == "human_approval_required"
    assert result["safety_review"]["execution_authorized"] is False
    assert "recommendation" in result["safety_review"]["reason"].lower()


def test_recommendation_failure_requires_human_review():
    state = {
        "event": {
            "event_id": "TEST-RECOMMENDATION-FAILURE",
            "asset_tag": "CNC-MILL-03",
            "raw_text": "Vibration alert",
            "readings": {},
        },
        "recommendation": {
            "summary": "Recommendation generation failed."
        },
        "findings": [
            {"agent": "researcher", "status": "success"},
            {"agent": "maintenance", "status": "error"},
        ],
    }

    result = safety_reviewer_agent(state)

    assert result["approval_required"] is True
    assert result["safety_review"]["status"] == "human_approval_required"
    assert result["safety_review"]["execution_authorized"] is False
    assert "recommendation" in result["safety_review"]["reason"].lower()




def test_ammonia_leak_requires_human_review_without_specific_manual():
    state = {
        "event": {
            "event_id": "TEST-AMMONIA-LEAK",
            "asset_tag": "LINE-3",
            "raw_text": (
                "The ammonia refrigeration skid on LINE-3 "
                "is leaking at the flange. What's the isolation "
                "procedure for that unit?"
            ),
            "readings": {},
        },
        "recommendation": {
            "summary": "No ammonia-specific isolation procedure found."
        },
        "findings": [
            {"agent": "researcher", "status": "success"},
            {"agent": "manual_rag", "status": "success"},
        ],
    }

    result = safety_reviewer_agent(state)

    assert result["approval_required"] is True
    assert result["safety_review"]["status"] == "human_approval_required"
    assert result["safety_review"]["execution_authorized"] is False
    assert "ammonia" in result["safety_review"]["reason"].lower()



def test_hydraulic_factual_question_does_not_trigger_safety_review():
    state = {
        "event": {
            "event_id": "TEST-HYD-FACTUAL",
            "asset_tag": "HYD-PRESS-02",
            "raw_text": (
                "What is the specified tightening torque "
                "for the hydraulic press flange bolts?"
            ),
            "readings": {},
        },
        "recommendation": {"summary": "Retrieve the documented specification."},
        "findings": [
            {"agent": "researcher", "status": "success"},
            {"agent": "manual_rag", "status": "success"},
        ],
    }

    result = safety_reviewer_agent(state)

    assert result["approval_required"] is False
    assert result["safety_review"]["status"] == "review_passed"
    assert result["safety_review"]["execution_authorized"] is False


def test_confined_space_threshold_question_does_not_trigger_review():
    question = (
        "What baseline atmospheric oxygen volume percentage threshold "
        "is required before commencing work in a confined space "
        "under the Permit to Work Standard?"
    )

    assert is_factual_standards_question(question) is True
    assert is_high_risk_maintenance_request(question) is False


def test_high_voltage_contactor_replacement_requires_review():
    question = (
        "Replace the main drive contactor on the conveyor. "
        "What authorization and electrical isolation are required "
        "under the high-voltage Permit to Work procedure?"
    )

    assert is_high_risk_maintenance_request(question) is True