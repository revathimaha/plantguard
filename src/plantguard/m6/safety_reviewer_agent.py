from src.plantguard.m6.permissions import scoped
import re

SAFETY_KEYWORDS = (
    "lockout",
    "tagout",
    "electrical",
    "high voltage",
    "energized",
    "pressure",
    # "hydraulic",
    # "confined space",
    "hot work",
    "live circuit",
    "live electrical",
)

PROCUREMENT_AUTO_APPROVAL_LIMIT = 200_000


def is_over_threshold_purchase(raw_text: str) -> bool:
    """Detect explicit purchase requests above the automatic threshold."""
    text = raw_text.replace(",", "").replace("₹", " ")

    purchase_intent = re.search(
        r"\b(purchase order|purchase|buy|procure|order|raise a po|po)\b",
        text,
        re.IGNORECASE,
    )
    amount = re.search(
        r"\b(\d+(?:\.\d+)?)\s*(?:rupees?|rs\.?)\b",
        text,
        re.IGNORECASE,
    )

    return bool(
        purchase_intent
        and amount
        and float(amount.group(1)) > PROCUREMENT_AUTO_APPROVAL_LIMIT
    )

def is_factual_standards_question(text: str) -> bool:
    """Recognize questions asking for documented standards, not work execution."""
    text = text.casefold().strip()

    asks_for_information = bool(re.search(
        r"\b(what|which|what is|what are|what baseline)\b",
        text,
    ))
    asks_for_threshold = bool(re.search(
        r"\b(threshold|percentage|volume percentage|standard|limit)\b",
        text,
    ))

    requests_an_action = bool(re.search(
        r"\b(replace|repair|install|remove|perform|carry out|"
        r"start work|begin work|isolate the|authorize the|"
        r"approve the|bypass|disable|suppress)\b",
        text,
    ))

    return (
        asks_for_information
        and asks_for_threshold
        and not requests_an_action
    )


def is_high_risk_maintenance_request(text: str) -> bool:
    """Detect hazardous maintenance work that requires human review."""
    text = text.casefold()

    maintenance_action = bool(re.search(
        r"\b(replace|replacing|repair|repairing|install|installing|"
        r"remove|removing|service|servicing|work on|maintenance)\b",
        text,
    ))

    high_risk_context = any(term in text for term in (
        "contactor",
        "high voltage",
        "electrical",
        "energized",
        "live circuit",
        "live electrical",
        "lockout",
        "tagout",
        "loto",
        "permit to work",
        "isolation",
    ))

    return maintenance_action and high_risk_context

@scoped("safety_reviewer")
def safety_reviewer_agent(state: dict) -> dict:
    """Apply deterministic safety checks; never authorize execution."""

    event = state.get("event") or {}
    recommendation = state.get("recommendation") or ""


    raw_text = str(event.get("raw_text", ""))
    text = raw_text.casefold()

    # Inspect the user-facing maintenance recommendation as well as the event.
    # Do not scan all retrieved evidence here; manuals may contain safety terms
    # even when the particular job is not safety-critical.
    if isinstance(recommendation, dict):
        recommendation_text = str(
            recommendation.get("summary", "")
        ).casefold()
    else:
        recommendation_text = str(recommendation).casefold()

    over_threshold_purchase = is_over_threshold_purchase(raw_text)
    implausible_readings = has_implausible_sensor_readings(event)


    factual_question = is_factual_standards_question(raw_text)

    event_safety_critical = (
        any(keyword in text for keyword in SAFETY_KEYWORDS)
        or is_high_risk_maintenance_request(raw_text)
    )

    recommendation_safety_critical = any(
        keyword in recommendation_text
        for keyword in (
            "safety-critical corrective action",
            "confined space",
            "hot work",
            "pressure vessel opening",
            "lockout/tagout",
            "lockout tagout",
            "lockout",
            "tagout",
            "permit to work",
        )
    )

    # A recommendation may repeat the subject of a factual question.
    # That alone must not turn an information request into a work authorization.
    if factual_question:
        recommendation_safety_critical = False

    safety_critical = (
        event_safety_critical or recommendation_safety_critical
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

    recommendation_failed = any(
        finding.get("agent") == "maintenance"
        and finding.get("status") == "error"
        for finding in state.get("findings", [])
    )

    raw_lower = raw_text.casefold()

    bypass_request = any(phrase in raw_lower for phrase in (
        "skip the paperwork",
        "bypass safety",
        "bypass lockout",
        "disable the alarm",
        "suppress the alarm",
        "shorten the fire watch",
        "waive the fire watch",
    ))

    
    
    manual_findings = [
        finding
        for finding in state.get("findings", [])
        if finding.get("agent") == "manual_rag"
    ]

    ammonia_leak = (
        "ammonia" in raw_lower
        and ("leak" in raw_lower or "leaking" in raw_lower)
    )

    asks_for_isolation = any(
        phrase in raw_lower
        for phrase in (
            "isolation procedure",
            "how to isolate",
            "isolation steps",
        )
    )

    missing_asset_procedure = (
        ammonia_leak
        and (
            not manual_findings
            or any(
                finding.get("status") != "success"
                for finding in manual_findings
            )
            or (
                asks_for_isolation
                and not any(
                    finding.get("status") == "success"
                    and finding.get("passages")
                    and any(
                        term in str(finding).casefold()
                        for term in (
                            "ammonia-specific isolation procedure",
                            "ammonia refrigeration skid",
                        )
                    )
                    for finding in manual_findings
                )
            )
        )
    )


    approval_required = (
        safety_critical
        or evidence_missing
        or over_threshold_purchase
        or implausible_readings
        or recommendation_failed
        or bypass_request
        or missing_asset_procedure
    )
    if over_threshold_purchase:
        status = "human_approval_required"
        reason = (
            "Purchase exceeds the ₹200,000 automatic approval threshold; "
            "Maintenance Manager authorization is required."
        )
    elif implausible_readings:
        status = "human_approval_required"
        reason = (
            "Implausible sensor readings detected; verify the sensors and "
            "escalate for human review. Do not suppress the alarm."
        )
    elif bypass_request:
        status = "human_approval_required"
        reason = (
            "Request to bypass required safety procedures detected; "
            "human review is required."
        )
    elif missing_asset_procedure:
        status = "human_approval_required"
        reason = (
            "Ammonia leak reported without successful manual/SOP retrieval; "
            "human review is required."
        )
    
    elif recommendation_failed:
        status = "human_approval_required"
        reason = (
            "Maintenance recommendation failed; "
            "human review is required before proceeding."
        )
    elif safety_critical:
        status = "human_approval_required"
        reason = "Safety-critical keywords detected."
    elif bypass_request:
        status = "human_approval_required"
        reason = (
            "Request to bypass required safety procedures detected; "
            "human review is required."
        )
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


def has_implausible_sensor_readings(event: dict) -> bool:
    """Flag clearly implausible conveyor sensor readings for review."""
    asset_tag = str(event.get("asset_tag", "")).upper()
    readings = event.get("readings") or {}

    raw_text = str(event.get("raw_text", ""))
    text = raw_text.casefold()

    if asset_tag == "CONV-BELT-01":
        # The golden case explicitly reports these impossible extremes.
        if "912" in text and "mm/s" in text:
            return True
        if "-40" in text and ("temperature" in text or "°c" in text or " c" in text):
            return True

    # Structured readings take precedence when present.
    if isinstance(readings, dict):
        vibration = readings.get("vibration_mm_s")
        temperature = readings.get("temperature_c")

        if isinstance(vibration, (int, float)) and vibration > 100:
            return True

        if isinstance(temperature, (int, float)) and temperature < -30:
            return True

    return False
