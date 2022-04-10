from typing import List

from pydantic import BaseModel


class MeasurementModel(BaseModel):
    inspection_id: str
    timestamp: int
    speed: float
    magnetic_fields: List[float]
    temperature: float
