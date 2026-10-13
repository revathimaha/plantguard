
import json
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_GOLDEN_SET = (
    PROJECT_ROOT / "data/plantguard/eval/golden_set.json"
)


def load_golden_set(path: Path = DEFAULT_GOLDEN_SET) -> list[dict[str, Any]]:
    """Load and validate the structural shape of the M8 golden set."""
    cases = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(cases, list) or len(cases) != 20:
        raise ValueError("M8 golden set must contain exactly 20 cases.")

    required_fields = {
        "id",
        "question",
        "expected",
        "category",
        "must_cite",
        "must_not_contain",
        "expected_route",
    }
    seen_ids = set()

    for case in cases:
        if not isinstance(case, dict):
            raise ValueError("Every golden case must be a JSON object.")

        missing = required_fields - case.keys()
        if missing:
            raise ValueError(
                f"Case is missing required fields: {sorted(missing)}"
            )

        if case["id"] in seen_ids:
            raise ValueError(f"Duplicate golden case ID: {case['id']}")
        seen_ids.add(case["id"])

        if case["expected_route"] not in {
            "auto", "human_review", "refuse"
        }:
            raise ValueError(
                f"Unsupported route for case {case['id']}: "
                f"{case['expected_route']}"
            )

    return cases


def evaluate_recorded_output(
    case: dict[str, Any],
    actual: dict[str, Any],
) -> dict[str, Any]:
    """
    Evaluate a recorded result.

    actual should contain:
      answer: final user-facing answer
      route: observed route (auto, human_review, or refuse)
      citations: list of source document titles explicitly cited
    """
    answer = str(actual.get("answer", ""))
    route = actual.get("route")
    citations = set(actual.get("citations", []))
    normalized_answer = answer.casefold()

    required_citations = set(case["must_cite"])
    prohibited_phrases = [
        phrase for phrase in case["must_not_contain"]
        if phrase.casefold() in normalized_answer
    ]

    missing_citations = sorted(required_citations - citations)

    checks = {
        "route_match": route == case["expected_route"],
        "citations_present": not missing_citations,
        "prohibited_phrases_absent": not prohibited_phrases,
        "answer_present": bool(answer.strip()),
    }

    return {
        "id": case["id"],
        "category": case["category"],
        "expected_route": case["expected_route"],
        "actual_route": route,
        "checks": checks,
        "missing_citations": missing_citations,
        "prohibited_phrases_found": prohibited_phrases,
        "passed": all(checks.values()),
    }


def main() -> None:
    cases = load_golden_set()
    print(f"Loaded {len(cases)} valid M8 golden scenarios.")

    print("Category counts:")
    for category in sorted({case["category"] for case in cases}):
        count = sum(case["category"] == category for case in cases)
        print(f"  {category}: {count}")

    print("Expected route counts:")
    for route in ("auto", "human_review", "refuse"):
        count = sum(case["expected_route"] == route for case in cases)
        print(f"  {route}: {count}")

    print(
        "\nGolden-set structure validated. No agent scenarios were run; "
        "recorded outputs must be supplied separately for behavior evaluation."
    )


if __name__ == "__main__":
    main()
