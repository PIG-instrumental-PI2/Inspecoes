from typing import List

from pydantic import BaseModel


class MeasurementModel(BaseModel):
    inspection_id: str
    ms_time: int
    speed: float
    magnetic_fields: List[float]
    temperature: float
