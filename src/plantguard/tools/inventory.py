import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def check_spare_parts(part_number: str) -> dict | None:
    """Return inventory information for a spare part."""

    inventory_path = (
        PROJECT_ROOT / "data/plantguard/mock_api/inventory.json"
    )

    with inventory_path.open("r", encoding="utf-8") as f:
        inventory = json.load(f)

    for part in inventory:
        if part["part_number"] == part_number:
            return part

    return None