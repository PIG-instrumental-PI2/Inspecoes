from typing import List

from repositories.measurements import MeasurementRepository
from schemas.charts import ChartsSchema
from services.data_input import MAGNETIC_FIELDS_COUNT
from utils.date_utils import HoursTimedelta
from utils.math_utils import avg, cal_new_pos, format_float


class ChartGroupService:
    def __init__(self) -> None:
        self._measurements_repository = MeasurementRepository()

    def get_measurements(self, inspection_id: str) -> List[ChartsSchema]:
        measurements = self._measurements_repository.get_by_inspection(inspection_id)

        temperatures = []
        speeds = []
        magnetic_fields = {
            f"magnetic_fields_{field}": [] for field in range(MAGNETIC_FIELDS_COUNT)
        }
        magnetic_fields_avg = []
        times = []
        times_formatted = []
        positions = []
        current_pos = 0
        measurements_last = len(measurements) - 1

        for index, measurement in enumerate(measurements):
            temperatures.append(measurement.temperature)
            speeds.append(measurement.speed)
            magnetic_fields_avg.append(avg(measurement.magnetic_fields))
            for field, key in enumerate(magnetic_fields.keys()):
                magnetic_fields[key].append(measurement.magnetic_fields[field])
            times.append(measurement.ms_time)
            times_formatted.append(
                str(HoursTimedelta(microseconds=measurement.ms_time * 1000))
            )
            positions.append(current_pos)

            current_pos = format_float(
                cal_new_pos(
                    initial_pos=current_pos,
                    begin_time_ms=measurements[index].ms_time,
                    final_time_ms=measurements[
                        min(index + 1, measurements_last)
                    ].ms_time,
                    speed=measurements[index].speed,
                )
            )

        return ChartsSchema(
            temperatures=temperatures,
            speeds=speeds,
            magnetic_fields_avg=magnetic_fields_avg,
            times=times,
            times_formatted=times_formatted,
            positions=positions,
            **magnetic_fields,
        )
