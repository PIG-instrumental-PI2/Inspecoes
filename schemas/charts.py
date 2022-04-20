from typing import List

from pydantic import BaseModel


################# Responses #################
class ChartsSchema(BaseModel):
    temperatures: List[float]
    speeds: List[float]
    magnetic_fields_avg: List[float]
    times: List[int]
    times_formatted: List[str]
