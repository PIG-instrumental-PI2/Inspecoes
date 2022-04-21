from typing import List

from repositories.processed_measurements import ProcessedMeasurementRepository
from schemas.charts import ChartsSchema
from services.data_input import MAGNETIC_FIELDS_COUNT


class ChartGroupService:
    def __init__(self) -> None:
        self._processed_measurements_repository = ProcessedMeasurementRepository()

    def get_measurements(self, inspection_id: str) -> ChartsSchema:
        measurements = self._processed_measurements_repository.get_by_inspection(
            inspection_id
        )

        temperatures = []
        speeds = []
        magnetic_fields = {
            f"magnetic_fields_{field}": [] for field in range(MAGNETIC_FIELDS_COUNT)
        }
        clustered_magnetic_fields = {
            f"clustered_magnetic_fields_{field}": []
            for field in range(MAGNETIC_FIELDS_COUNT)
        }
        magnetic_fields_avg = []
        times = []
        formatted_times = []
        positions = []

        for measurement in measurements:
            temperatures.append(measurement.temperature)
            times.append(measurement.ms_time)
            speeds.append(measurement.speed)
            magnetic_fields_avg.append(measurement.magnetic_fields_avg)
            magnetic_fields = self._append_fields_into_dict(
                magnetic_fields, measurement.magnetic_fields
            )
            clustered_magnetic_fields = self._append_fields_into_dict(
                clustered_magnetic_fields, measurement.clustered_magnetic_fields
            )
            # for field, key in enumerate(magnetic_fields.keys()):
            #     magnetic_fields[key].append(measurement.magnetic_fields[field])
            formatted_times.append(measurement.formatted_time)
            positions.append(measurement.position)

        return ChartsSchema(
            times=times,
            temperatures=temperatures,
            speeds=speeds,
            magnetic_fields_avg=magnetic_fields_avg,
            formatted_times=formatted_times,
            positions=positions,
            **magnetic_fields,
            **clustered_magnetic_fields,
        )

    def _append_fields_into_dict(self, fields_dict: dict, fields_array: list):
        for field, key in enumerate(fields_dict.keys()):
            fields_dict[key].append(fields_array[field])
        return fields_dict
