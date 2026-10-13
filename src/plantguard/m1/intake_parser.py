import time

from litellm import RateLimitError
from pydantic import ValidationError
from plantguard.llm.client import LLMClient
from plantguard.models.maintenance_event import MaintenanceEvent


class IntakeParser:
    """Parse raw maintenance intake into a validated MaintenanceEvent."""

    def __init__(self, llm_client: LLMClient, max_retries: int = 2):
        self.llm_client = llm_client
        self.max_retries = max_retries

    def parse_all(
    self,
    records: list[dict],
) -> tuple[list[MaintenanceEvent], list[tuple[dict, Exception]]]:

        valid_events = []
        failed_records = []

        for record in records:
            try:
                event = self.parse(record)
                valid_events.append(event)

            except RateLimitError as error:
                print(
                    f"Rate limit reached while processing "
                    f"{record.get('event_id')}")
                failed_records.append((record, error))
               
            except Exception as error:
                print(
                    f"Failed event: {record.get('event_id')}"
                )
                print(
                    f"Exception type: {type(error).__name__}"
                )
                print(
                    f"Exception: {error}"
                )

                failed_records.append((record, error))

        return valid_events, failed_records

    def parse(self, record: dict) -> MaintenanceEvent:
        prompt = f"""
Parse the following maintenance event into a JSON object.

Return exactly these fields:
- event_id
- source
- received_at
- asset_code
- asset_tag
- raw_text
- readings

The readings object must contain:
- vibration_mm_s
- temp_c
- pressure_bar
- current_a

Preserve values from the input.
Do not invent missing sensor readings.
Use null when a reading is missing.

Input maintenance event:
{record}
"""

        for attempt in range(self.max_retries + 1):
            result = self.llm_client.complete_json(prompt)

            try:
                return MaintenanceEvent.model_validate(result)

            except ValidationError as error:
                prompt = f"""
Your previous response could not be validated.

Validation error:
{error}

Fix the JSON so that it satisfies the required MaintenanceEvent schema.

Return only the corrected JSON object.

Original maintenance event:
{record}

Previous response:
{result}
"""

        raise ValueError(
            f"Could not produce a valid MaintenanceEvent "
            f"after {self.max_retries + 1} attempts."
        )


