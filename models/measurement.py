from typing import List, Optional

from pydantic import BaseModel


class MeasurementModel(BaseModel):
    inspection_id: Optional[str]
    ms_time: Optional[int]
    temperature: Optional[float]
    speed: Optional[float]
    magnetic_fields: Optional[List[float]]


class ProcessedMeasurementsModel(BaseModel):
    inspection_id: Optional[str]
    ms_time: Optional[int]
    formatted_time: Optional[str]
    position: Optional[float]
    temperature: Optional[float]
    speed: Optional[float]
    magnetic_fields: Optional[List[float]]
    magnetic_fields_avg: Optional[float]
    clustered_magnetic_fields_avg: Optional[int]
