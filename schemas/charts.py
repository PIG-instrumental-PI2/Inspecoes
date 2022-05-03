from typing import List, Optional

from pydantic import BaseModel


################# Responses #################
class ChartsSchema(BaseModel):
    times: List[int]
    temperatures: List[float]
    speeds: List[float]
    magnetic_fields_avg: List[float]
    clustered_magnetic_avg: List[float]
    formatted_times: List[str]
    positions: List[float]
    clusters: List[list] = []
