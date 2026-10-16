import json
import os
from pathlib import Path

from langfuse import get_client

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT / "data/plantguard/eval/behavioral_results.json"


def main():
    if not os.getenv("LANGFUSE_PUBLIC_KEY") or not os.getenv("LANGFUSE_SECRET_KEY"):
        raise SystemExit(
            "Missing Langfuse credentials. Configure them in this terminal."
        )

    if not RESULTS.exists():
        raise SystemExit(f"Results file not found: {RESULTS}")

    payload = json.loads(RESULTS.read_text(encoding="utf-8"))
    records = payload.get("results", [])

    if not records:
        raise SystemExit("No recorded M8 results found.")

    required = {
        "id", "actual_route", "route_match",
        "missing_required_citations", "prohibited_phrases_found",
        "answer_present", "passed",
    }

    for record in records:
        if not required.issubset(record):
            raise SystemExit(
                f"Case {record.get('id', '?')} has unexpected fields. "
                "Nothing was published."
            )

    client = get_client()

    for record in records:
        with client.start_as_current_observation(
            as_type="span",
            name=f"PlantGuard M8 evaluation {record['id']}",
            input={"question": record.get("question", "")},
            output={
                "actual_route": record["actual_route"],
                "passed": record["passed"],
                "historical_result": True,
            },
            metadata={
                "case_id": record["id"],
                "category": record.get("category"),
                "expected_route": record.get("expected_route"),
                "recorded_at": payload.get("generated_at"),
            },
        ) as span:
            metrics = {
                "route_match": record["route_match"],
                "citation_recall": not record["missing_required_citations"],
                "prohibited_phrases_absent": not record["prohibited_phrases_found"],
                "answer_present": record["answer_present"],
                "case_passed": record["passed"],
            }

            for name, value in metrics.items():
                span.score_trace(
                    name=name,
                    value=1.0 if value else 0.0,
                    data_type="NUMERIC",
                )

    client.flush()

    print(f"Published {len(records)} historical M8 traces to Langfuse.")
    print("Open Langfuse -> Traces to inspect them.")
    print("No agent or LLM evaluation was rerun.")


if __name__ == "__main__":
    main()
