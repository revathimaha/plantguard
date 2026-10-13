from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SensorReadings(BaseModel):
    vibration_mm_s: Optional[float] = None
    temp_c: Optional[float] = None
    pressure_bar: Optional[float] = None
    current_a: Optional[float] = None


class MaintenanceEvent(BaseModel):
    event_id: str
    source: str
    received_at: datetime

    asset_code: str
    asset_tag: str

    raw_text: str

    readings: SensorReadings