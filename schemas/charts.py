from typing import List

from pydantic import BaseModel


################# Responses #################
class ChartsSchema(BaseModel):
    temperatures: List[float]
    speeds: List[float]
    magnetic_fields_avg: List[float]
    times: List[int]
    times_formatted: List[str]
    positions: List[float]
    magnetic_fields_0: List[float] = []
    magnetic_fields_1: List[float] = []
    magnetic_fields_2: List[float] = []
    magnetic_fields_3: List[float] = []
    magnetic_fields_4: List[float] = []
    magnetic_fields_5: List[float] = []
    magnetic_fields_6: List[float] = []
    magnetic_fields_7: List[float] = []
    magnetic_fields_8: List[float] = []
    magnetic_fields_9: List[float] = []
    magnetic_fields_10: List[float] = []
    magnetic_fields_11: List[float] = []
    magnetic_fields_12: List[float] = []
    magnetic_fields_13: List[float] = []
    magnetic_fields_14: List[float] = []
    magnetic_fields_15: List[float] = []
