from src.plantguard.m6.permissions import scoped


SAFETY_KEYWORDS = (
    "lockout",
    "tagout",
    "electrical",
    "high voltage",
    "energized",
    "pressure",
    "hydraulic",
    "confined space",
    "hot work",
    "live circuit",
    "live electrical",
)


@scoped("safety_reviewer")
def safety_reviewer_agent(state: dict) -> dict:
    """Apply deterministic safety checks; never authorize execution."""

    event = state.get("event") or {}
    recommendation = state.get("recommendation") or ""

    raw_text = str(event.get("raw_text", ""))
    text = f"{raw_text} {recommendation}".lower()

    safety_critical = any(
        keyword in text for keyword in SAFETY_KEYWORDS
    )

    researcher_findings = [
        finding
        for finding in state.get("findings", [])
        if finding.get("agent") == "researcher"
    ]

    evidence_missing = not researcher_findings or any(
        finding.get("status") != "success"
        for finding in researcher_findings
    )

    approval_required = safety_critical or evidence_missing

    if safety_critical:
        status = "human_approval_required"
        reason = "Safety-critical keywords detected."
    elif evidence_missing:
        status = "escalation_required"
        reason = "Research evidence is missing or unavailable."
    else:
        status = "review_passed"
        reason = "No configured safety-critical trigger detected."

    return {
        "safety_review": {
            "status": status,
            "safety_critical": safety_critical,
            "evidence_missing": evidence_missing,
            "reason": reason,
            "execution_authorized": False,
        },
        "approval_required": approval_required,
        "audit_log": [
            f"safety_reviewer: {status}; execution remains unauthorized"
        ],
    }
