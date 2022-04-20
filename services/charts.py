from typing import List

from repositories.measurements import MeasurementRepository
from schemas.charts import ChartsSchema
from utils.math_utils import avg


class ChartGroupService:
    def __init__(self) -> None:
        self._measurements_repository = MeasurementRepository()

    def get_charts(self, inspection_id: str) -> List[ChartsSchema]:
        measurements = self._measurements_repository.get_by_inspection(inspection_id)

        temperatures = []
        speeds = []
        magnetic_fields_avg = []
        times = []

        for measurement in measurements:
            temperatures.append(measurement.temperature)
            speeds.append(measurement.speed)
            magnetic_fields_avg.append(avg(measurement.magnetic_fields))
            times.append(measurement.ms_time)

        return ChartsSchema(
            temperatures=temperatures,
            speeds=speeds,
            magnetic_fields_avg=magnetic_fields_avg,
            times=times,
        )
