from src.plantguard.m6.permissions import scoped


def recommendation_reviewer_agent(state: dict) -> dict:
    """Deterministically check recommendation claims against supplied evidence."""

    recommendation = state.get("recommendation")
    findings = state.get("findings", [])

    researcher_findings = [
        item for item in findings
        if item.get("agent") == "researcher"
        and item.get("status") == "success"
    ]

    maintenance_findings = [
        item for item in findings
        if item.get("agent") == "maintenance"
        and item.get("status") == "success"
    ]

    issues = []

    if not researcher_findings:
        issues.append("Successful researcher evidence is missing.")

    if not maintenance_findings:
        issues.append("Successful maintenance recommendation is missing.")

    if not isinstance(recommendation, dict):
        issues.append("Recommendation is not a structured object.")
    else:
        required_fields = {
            "summary",
            "evidence",
            "possible_causes",
            "recommended_next_steps",
            "evidence_gaps",
            "human_review_recommended",
        }

        missing = required_fields - recommendation.keys()
        if missing:
            issues.append(
                "Recommendation fields missing: "
                + ", ".join(sorted(missing))
            )

        evidence = recommendation.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            issues.append("Recommendation contains no evidence entries.")

        for entry in evidence if isinstance(evidence, list) else []:
            if not isinstance(entry, dict) or not entry.get("source"):
                issues.append(
                    "An evidence entry is missing its source description."
                )
                break

    passed = not issues

    review = {
        "status": "passed" if passed else "revision_required",
        "passed": passed,
        "issues": issues,
        "execution_authorized": False,
    }

    return {
        "recommendation_review": review,
        "findings": [{
            "agent": "recommendation_reviewer",
            "status": review["status"],
            "issues": issues,
        }],
        "audit_log": [
            "recommendation_reviewer: "
            + ("structural review passed" if passed
               else "revision requested")
            + "; no action authorized"
        ],
    }