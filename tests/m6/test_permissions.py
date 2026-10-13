import pytest

from src.plantguard.m6.permissions import validate_agent_update


def test_researcher_cannot_change_safety_approval():
    with pytest.raises(PermissionError):
        validate_agent_update(
            "researcher",
            {"approval_required": False},
        )


def test_maintenance_cannot_change_procurement_result():
    with pytest.raises(PermissionError):
        validate_agent_update(
            "maintenance",
            {"procurement_result": {"available": True}},
        )


def test_unknown_agent_is_rejected():
    with pytest.raises(ValueError):
        validate_agent_update(
            "unknown_agent",
            {"findings": []},
        )


def test_agent_can_update_authorized_field():
    update = {"findings": [{"source": "sensor_history"}]}

    result = validate_agent_update("researcher", update)

    assert result == update
