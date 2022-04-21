from typing import List, Optional

from pydantic import BaseModel


################# Responses #################
class ChartsSchema(BaseModel):
    times: List[int]
    temperatures: List[float]
    speeds: List[float]
    magnetic_fields_avg: List[float]
    formatted_times: List[str]
    positions: List[float]
    clusters: List[list] = []
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
    clustered_magnetic_fields_0: List[float] = []
    clustered_magnetic_fields_1: List[float] = []
    clustered_magnetic_fields_2: List[float] = []
    clustered_magnetic_fields_3: List[float] = []
    clustered_magnetic_fields_4: List[float] = []
    clustered_magnetic_fields_5: List[float] = []
    clustered_magnetic_fields_6: List[float] = []
    clustered_magnetic_fields_7: List[float] = []
    clustered_magnetic_fields_8: List[float] = []
    clustered_magnetic_fields_9: List[float] = []
    clustered_magnetic_fields_10: List[float] = []
    clustered_magnetic_fields_11: List[float] = []
    clustered_magnetic_fields_12: List[float] = []
    clustered_magnetic_fields_13: List[float] = []
    clustered_magnetic_fields_14: List[float] = []
    clustered_magnetic_fields_15: List[float] = []
