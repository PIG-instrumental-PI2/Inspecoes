from typing import List, Optional

from pydantic import BaseModel


class MeasurementModel(BaseModel):
    inspection_id: str
    ms_time: int
    temperature: float
    speed: float
    magnetic_fields: List[float]


class ProcessedMeasurementsModel(BaseModel):
    inspection_id: str
    ms_time: int
    formatted_time: str
    position: float
    temperature: float
    speed: float
    magnetic_fields: List[float]
    magnetic_fields_avg: float
    clustered_magnetic_fields: Optional[List[int]] = []
