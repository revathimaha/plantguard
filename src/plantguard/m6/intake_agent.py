from src.plantguard.m6.permissions import scoped


@scoped("intake")
def intake_agent(state: dict) -> dict:
    """Normalize the incoming event for the PlantGuard specialist team."""
    event = state.get("event")

    if not isinstance(event, dict):
        return {
            "error": "Missing or invalid maintenance event.",
            "audit_log": ["intake: rejected missing or invalid event"],
        }

    required_fields = (
        "event_id",
        "asset_tag",
        "raw_text",
        "readings",
    )
    missing = [field for field in required_fields if field not in event]

    if missing:
        return {
            "error": f"Missing event fields: {', '.join(missing)}",
            "audit_log": ["intake: rejected incomplete event"],
        }

    plan = [
        "researcher: retrieve relevant sensor history and maintenance evidence",
        "maintenance: propose an evidence-based maintenance recommendation",
        "procurement: check spare-part availability if needed",
        "safety_reviewer: independently review safety and approval requirements",
    ]

    return {
        "plan": plan,
        "findings": [
            {
                "agent": "intake",
                "event_id": event["event_id"],
                "asset_tag": event["asset_tag"],
                "raw_text": event["raw_text"],
                "readings": event["readings"],
            }
        ],
        "audit_log": [
            f"intake: accepted event {event['event_id']} "
            f"for asset {event['asset_tag']}"
        ]
    }