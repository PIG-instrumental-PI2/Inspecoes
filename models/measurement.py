from datetime import datetime
from typing import List

from pydantic import BaseModel


class MeasurementModel(BaseModel):
    inspection_id: str
    timestamp: datetime
    speed: float
    magnetic_fields: List[float]
    temperature: float
