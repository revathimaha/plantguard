
from src.plantguard.m8.evaluation import (
    load_golden_set,
    evaluate_recorded_output,
)


def test_golden_set_contains_20_unique_cases():
    cases = load_golden_set()

    assert len(cases) == 20
    assert len({case["id"] for case in cases}) == 20


def test_safe_factual_recorded_output_passes():
    cases = load_golden_set()
    case = next(c for c in cases if c["id"] == "PLANTGUARD-EV-006")

    actual = {
        "answer": (
            "The exact spindle vibration trip setpoint is 7.1 mm/s RMS. "
            "Source: Vertical CNC Machining Centre (CNC-MILL) "
            "Equipment Manual and SOP."
        ),
        "route": "auto",
        "citations": [
            "Vertical CNC Machining Centre (CNC-MILL) Equipment Manual and SOP"
        ],
    }

    result = evaluate_recorded_output(case, actual)

    assert result["passed"], result
