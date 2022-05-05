from repositories.processed_measurements import ProcessedMeasurementRepository
from schemas.charts import ChartsSchema


class ChartGroupService:
    def __init__(self) -> None:
        self._processed_measurements_repository = ProcessedMeasurementRepository()

    def get_measurements(
        self, inspection_id: str, start_time: int = None, finish_time: int = None
    ) -> ChartsSchema:
        measurements = self._processed_measurements_repository.get_by_inspection(
            inspection_id, start_time, finish_time
        )

        temperatures = []
        speeds = []
        clustered_magnetic_fields_avg = []
        magnetic_fields_avg = []
        times = []
        formatted_times = []
        positions = []

        for measurement in measurements:
            temperatures.append(measurement.temperature)
            times.append(measurement.ms_time)
            speeds.append(measurement.speed)
            magnetic_fields_avg.append(measurement.magnetic_fields_avg)
            clustered_magnetic_fields_avg.append(
                measurement.clustered_magnetic_fields_avg
            )
            formatted_times.append(measurement.formatted_time)
            positions.append(measurement.position)

        return ChartsSchema(
            times=times,
            temperatures=temperatures,
            speeds=speeds,
            magnetic_fields_avg=magnetic_fields_avg,
            formatted_times=formatted_times,
            positions=positions,
            clustered_magnetic_fields_avg=clustered_magnetic_fields_avg,
        )

    def _append_fields_into_dict(self, fields_dict: dict, fields_array: list):
        for field, key in enumerate(fields_dict.keys()):
            try:
                fields_dict[key].append(fields_array[field])
            except:
                pass
        return fields_dict
