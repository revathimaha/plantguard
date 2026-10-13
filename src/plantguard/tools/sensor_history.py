import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def get_sensor_history(
    asset_tag: str,
    limit: int = 10,
) -> list[dict]:
    """Return recent telemetry records for an asset."""

    telemetry_path = (
        PROJECT_ROOT / "data/plantguard/mock_api/telemetry.json"
    )

    with telemetry_path.open("r", encoding="utf-8") as f:
        telemetry = json.load(f)

    records = [
        record
        for record in telemetry
        if record["asset_tag"] == asset_tag
    ]

    records.sort(
        key=lambda record: record["hour_index"],
        reverse=True,
    )

    return records[:limit]