import pytest

from src.plantguard.m4.service import PlantGuardRetrievalService


def make_service():
    service = PlantGuardRetrievalService.__new__(PlantGuardRetrievalService)
    service.final_limit = 5
    service.all_chunks = [
        {
            "text": f"Canonical content for {source}",
            "metadata": {"source": source},
        }
        for source in (
            "alarm-response.md",
            "lockout-tagout.md",
            "permit-to-work.md",
        )
    ]
    return service


def returned_sources(results):
    sources = []
    for item in results:
        current = item
        while isinstance(current, dict) and "result" in current:
            current = current["result"]
        if isinstance(current, dict) and "chunk" in current:
            sources.append(current["chunk"].get("metadata", {}).get("source"))
    return set(sources)


@pytest.mark.parametrize(
    ("question", "expected_sources"),
    [
        (
            "HYD-PRESS-02 high vibration, skip the paperwork",
            {"lockout-tagout.md", "permit-to-work.md"},
        ),
        (
            "CONV-BELT-01 sensor fault; can I suppress the alarm?",
            {"alarm-response.md"},
        ),
        (
            "What's the bearing replacement torque spec and does the job need a permit?",
            {"permit-to-work.md"},
        ),
    ],
)
def test_question_intent_adds_required_safety_documents(question, expected_sources):
    service = make_service()

    results = service._add_safety_standard_coverage(question, [])

    assert expected_sources <= returned_sources(results)


def test_existing_results_are_preserved_when_space_allows():
    service = make_service()
    existing = {
        "result": {
            "chunk": {
                "text": "asset manual content",
                "metadata": {"source": "manual-air-comp.md"},
            },
            "score": 1.0,
        },
        "rerank_score": 1.0,
    }

    results = service._add_safety_standard_coverage(
        "Does this job need a permit?", [existing]
    )

    assert results[0] is existing
    assert "permit-to-work.md" in returned_sources(results)
