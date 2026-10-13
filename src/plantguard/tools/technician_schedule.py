import json
from pathlib import Path


def get_technician_schedule(
    technician_id: str,
    date: str | None = None,
) -> list[dict]:
    """Return technician availability from the calendar."""

    calendar_path = Path(
        "data/plantguard/mock_api/technician_calendar.json"
    )

    with calendar_path.open("r", encoding="utf-8") as f:
        calendar = json.load(f)

    records = [
        entry
        for entry in calendar
        if entry["technician_id"] == technician_id
    ]

    if date is not None:
        records = [
            entry
            for entry in records
            if entry["date"] == date
        ]

    return records