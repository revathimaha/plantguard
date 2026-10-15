import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GOLDEN = ROOT / "data/plantguard/eval/golden_set.json"
OUTPUT = ROOT / "data/plantguard/eval/behavioral_results.json"


def collect_asset_tags(value):
    tags = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "asset_tag" and isinstance(item, str):
                tags.add(item)
            tags.update(collect_asset_tags(item))
    elif isinstance(value, list):
        for item in value:
            tags.update(collect_asset_tags(item))
    return tags


def find_asset(question, tags):
    q = question.casefold()
    for tag in sorted(tags, key=len, reverse=True):
        if tag.casefold() in q:
            return tag

    hints = [
        (("chiller",), "CHILLER"),
        (("ammonia", "line-3"), "LINE-3"),
        (("hyd-press", "hydraulic press"), "HYD-PRESS-02"),
        (("conv-belt", "conveyor belt", "belt contactor"), "CONV-BELT-01"),
        (("air-comp", "compressor"), "AIR-COMP"),
        (("ind-oven", "industrial oven"), "IND-OVEN"),
        (("pump-cent", "centrifugal pump"), "PUMP-CENT"),
        (("robot-weld",), "ROBOT-WELD"),
        (("cnc", "spindle"), "CNC-MILL-01"),
    ]
   
    for words, tag in hints:
        if any(word in q for word in words):
            return tag
    return "UNKNOWN-ASSET"

def load_citation_aliases():
    """Map corpus document titles and filenames to canonical titles."""
    index_path = ROOT / "data/plantguard/corpus/index.json"
    documents = json.loads(index_path.read_text(encoding="utf-8"))

    aliases = {}
    for document in documents:
        title = document.get("title", "")
        slug = document.get("slug", "")
        markdown = Path(document.get("markdown", "")).name
        pdf = Path(document.get("pdf", "")).name

        for alias in (title, slug, markdown, pdf):
            if alias:
                aliases[alias.casefold()] = title.casefold()

    return aliases


def main():
    from src.plantguard.m6.graph import build_graph
    import src.plantguard.observability.tracing as tracing

    # Keep this evaluation local; avoid repeated failed cloud-export attempts.
    tracing.LOCAL_ONLY = True

    cases = json.loads(GOLDEN.read_text(encoding="utf-8"))
    assets_file = ROOT / "data/plantguard/mock_api/assets.json"
    assets = json.loads(assets_file.read_text(encoding="utf-8"))
    tags = collect_asset_tags(assets)

    graph = build_graph()
    records = []

    for index, case in enumerate(cases, 1):
        question = case["question"]
        asset_tag = find_asset(question, tags)
        print(f"[{index}/{len(cases)}] {case['id']} — {asset_tag}", flush=True)

        record = {
            "id": case["id"],
            "question": question,
            "category": case["category"],
            "expected_route": case["expected_route"],
            "asset_tag_used": asset_tag,
        }

        try:
            result = graph.invoke(
                {
                    "event": {
                        "event_id": case["id"],
                        "asset_tag": asset_tag,
                        "raw_text": question,
                        "readings": {},
                    }
                },
                config={
                    "configurable": {"thread_id": f"m8-{case['id']}"},
                    "recursion_limit": 30,
                },
            )

            recommendation = result.get("recommendation") or {}
            answer = (
                recommendation.get("summary", "")
                if isinstance(recommendation, dict)
                else str(recommendation or "")
            )

            citations = []
            if isinstance(recommendation, dict):
                citations.extend(
                    item.get("source", "")
                    for item in recommendation.get("evidence", [])
                    if isinstance(item, dict) and item.get("source")
                )

            findings = result.get("findings", [])
            for finding in findings:
                if finding.get("agent") == "manual_rag":
                    citations.extend(
                        item.get("source", "")
                        for item in finding.get("passages", [])
                        if item.get("source")
                    )

            citations = sorted(set(citations))
            refusal = (
                recommendation.get("refusal", {})
                if isinstance(recommendation, dict)
                else {}
            )
            interrupted = bool(result.get("__interrupt__"))
            approval_required = bool(result.get("approval_required"))

            # An actual interrupt remains a human-review route.
            # Otherwise, an explicit refusal is distinct from human approval.
            # Check only the user-facing answer.
            full_answer = answer

            if interrupted:
                actual_route = "human_review"
            elif refusal.get("refused") is True and result.get("status") == "refused":
                actual_route = "refuse"
            elif approval_required:
                actual_route = "human_review"
            else:
                actual_route = "auto"

            prohibited = [
                phrase
                for phrase in case["must_not_contain"]
                if phrase.casefold() in full_answer.casefold()
            ]

            citation_aliases = load_citation_aliases()

            def canonicalize_citation(value):
                value = value.casefold()
                for alias, canonical_title in citation_aliases.items():
                    if alias in value:
                        return canonical_title
                return value

            normalized_citations = [
                canonicalize_citation(citation)
                for citation in citations
            ]

            missing_citations = [
                title for title in case["must_cite"]
                if canonicalize_citation(title) not in normalized_citations
            ]

            record.update({
                "refusal": refusal,
                "status": result.get("status", "interrupted" if interrupted else "unknown"),
                "actual_route": actual_route,
                "route_match": actual_route == case["expected_route"],
                "approval_required": approval_required,
                "interrupted": interrupted,
                "answer": answer,
                "citations": citations,
                "safety_review": result.get("safety_review"),
                "procurement_result": result.get("procurement_result"),
                "error": result.get("error"),
                "missing_required_citations": missing_citations,
                "prohibited_phrases_found": prohibited,
                "answer_present": bool(answer.strip()),
            })
            record["passed"] = all([
                record["route_match"],
                not missing_citations,
                not prohibited,
                record["answer_present"],
                not record.get("error"),
                answer.strip() != "Recommendation generation failed. Escalate for human review.",
            ])

        except Exception as exc:
            record.update({
                "actual_route": "error",
                "status": "error",
                "error": f"{type(exc).__name__}: {exc}",
                "passed": False,
            })

        records.append(record)

        # Persist progress after every case so interrupted runs are recoverable.
        OUTPUT.write_text(
            json.dumps({
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "evaluation_scope": "Actual M6 graph executions; not expected-answer fixtures.",
                "total_cases": len(cases),
                "completed_cases": len(records),
                "results": records,
            }, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        time.sleep(1)

    passed = sum(record.get("passed", False) for record in records)
    errors = sum(record.get("status") == "error" for record in records)

    print(f"\nFinished: {len(records)}/{len(cases)} cases recorded.")
    print(f"Passed all implemented checks: {passed}/{len(records)}")
    print(f"Execution errors: {errors}")
    print(f"Results: {OUTPUT}")
    print("Note: refusal routes are evaluated separately from human-review routes.")
if __name__ == "__main__":
    main()
