import json

from pydantic import ValidationError
from plantguard.tools.sensor_history import get_sensor_history
from plantguard.tools.downtime_cost import calculate_downtime_cost
from plantguard.tools.inventory import check_spare_parts
from plantguard.tools.technician_schedule import (
    get_technician_schedule,
)
from plantguard.models.maintenance_event import MaintenanceEvent
from plantguard.llm.client import LLMClient
from plantguard.m1.intake_parser import IntakeParser

def load_records(file_path: str) -> list[dict]:
    """Load multiple JSON objects from the intake file."""

    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    decoder = json.JSONDecoder()
    pos = 0
    records = []

    while pos < len(content):
        while pos < len(content) and content[pos].isspace():
            pos += 1

        if pos >= len(content):
            break

        record, pos = decoder.raw_decode(content, pos)
        records.append(record)

    return records

def test_downtime_cost():
    cost = calculate_downtime_cost(
        downtime_hours=4,
        cost_per_hour=15000,
    )

    print("Downtime cost:", cost)

def validate_record(record: dict) -> MaintenanceEvent:
    """Validate one raw record and return a MaintenanceEvent."""

    return MaintenanceEvent.model_validate(record)


def validate_all_records(
    records: list[dict],
) -> tuple[list[MaintenanceEvent], list[tuple[dict, ValidationError]]]:
    """Validate all records and separate valid and invalid records."""

    valid_events = []
    invalid_records = []

    for record in records:
        try:
            event = validate_record(record)
            valid_events.append(event)

        except ValidationError as error:
            invalid_records.append((record, error))

    return valid_events, invalid_records

def test_sensor_history():
    history = get_sensor_history(
        asset_tag="VPW-CNC-MILL-03",
        limit=5,
    )

    print("\nSensor history:")
    for record in history:
        print(record)


def main():
    test_sensor_history()
    test_downtime_cost()
    result = check_spare_parts("VPW-P-00001")
    print(result)


    technician_result = get_technician_schedule(
        technician_id="VPW-T-001",
        date="2026-08-12",  
    )

    print("Technician schedule:")

    for entry in technician_result[:10]:
        print(entry)

    records = load_records(
        "data/plantguard/intake/records.jsonl"
    )

    client = LLMClient(
        model="groq/openai/gpt-oss-20b",
        api_key="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",
    )

    parser = IntakeParser(client)

    events, failures = parser.parse_all(records[:15])

    print(f"Total records: {len(records)}")
    print(f"Successfully parsed: {len(events)}")
    print(f"Failed: {len(failures)}")

    for record, error in failures:
        print(f"Failed event: {record.get('event_id')}")
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
