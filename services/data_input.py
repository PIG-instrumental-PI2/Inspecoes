from typing import List

import numpy as np
from sklearn.cluster import KMeans

from libraries.crc_utils import CRCUtils
from models.measurement import MeasurementModel, ProcessedMeasurementsModel
from repositories.measurements import MeasurementRepository
from utils.date_utils import HoursTimedelta
from utils.math_utils import avg, cal_new_pos, format_float

MAGNETIC_FIELDS_COUNT = 16
# Sizes in byte
TIME_SIZE = 4
SPEED_SIZE = 4
MAGNETIC_FIELD_SIZE = 4
TEMPERATURE_SIZE = 4
READING_SIZE = (
    TIME_SIZE
    + SPEED_SIZE
    + MAGNETIC_FIELD_SIZE * MAGNETIC_FIELDS_COUNT
    + TEMPERATURE_SIZE
)
CLUSTERS_COUNT = 5


class DataInputService:
    def __init__(self) -> None:
        self._measurements_repository = MeasurementRepository()

    def upload_data(self, inspection_id: str, encoded_data: bytes) -> bool:
        corrupted = False

        try:
            data_bytes, crc = CRCUtils.get_data(encoded_data)
            if CRCUtils.check_integrity(data_bytes, crc):
                for measurement_bytes in self._get_measurements(data_bytes):
                    measurement = self._parse_measurement(measurement_bytes)
                    self._measurements_repository.save(
                        MeasurementModel(
                            inspection_id=inspection_id,
                            ms_time=measurement.get("time"),
                            speed=measurement.get("speed"),
                            magnetic_fields=measurement.get("magnetic_fields"),
                            temperature=measurement.get("temperature"),
                        )
                    )
            else:
                raise TypeError()
        except Exception as ex:
            corrupted = True

        return corrupted

    def post_processing(self, inspection_id):
        """Peform post processing on inspection data"""
        processed_measurements = self._transform_measurements(inspection_id)
        clustered_magnetic_fields_0 = self._clustering(
            processed_measurements.magnetic_fields_0
        )

    def _transform_measurements(self, inspection_id: str):
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

        return ProcessedMeasurementsModel(
            temperatures=temperatures,
            speeds=speeds,
            magnetic_fields_avg=magnetic_fields_avg,
            times=times,
            times_formatted=times_formatted,
            positions=positions,
            **magnetic_fields,
        )

    def _clustering(self, magnetic_field_one_dimension: List[float]):
        magnetic_field_one_dimension: np.array = np.array(
            magnetic_field_one_dimension
        ).reshape(-1, 1)
        kmeans = KMeans(n_clusters=CLUSTERS_COUNT, random_state=42).fit(
            magnetic_field_one_dimension
        )
        # centers = kmeans.cluster_centers_
        # data_test = magnetic_field_one_dimension[:5, :].reshape(-1, 1)
        # kmeans_predicted = kmeans.predict(data_test)

        # Save pickle

    def _get_measurements(self, data_bytes: bytes):
        begin = 0
        end = 0
        while True:
            begin = end
            end = begin + READING_SIZE
            measurement = data_bytes[begin:end]
            if not measurement:
                break
            yield measurement

    def _parse_measurement(self, data_bytes: bytes) -> dict:
        begin_pos = 0
        end_pos = begin_pos + TIME_SIZE

        time_data = CRCUtils.int_from_bytes(data_bytes[begin_pos:end_pos])

        begin_pos = end_pos
        end_pos = begin_pos + SPEED_SIZE
        speed_data = format_float(
            CRCUtils.float_from_bytes(data_bytes[begin_pos:end_pos])
        )

        magnetic_fields = []
        for _ in range(MAGNETIC_FIELDS_COUNT):
            begin_pos = end_pos
            end_pos = begin_pos + MAGNETIC_FIELD_SIZE
            magnetic_fields.append(
                format_float(CRCUtils.float_from_bytes(data_bytes[begin_pos:end_pos]))
            )

        begin_pos = end_pos
        end_pos = begin_pos + TEMPERATURE_SIZE
        temperature_data = format_float(
            CRCUtils.float_from_bytes(data_bytes[begin_pos:end_pos])
        )

        return {
            "time": time_data,
            "speed": speed_data,
            "magnetic_fields": magnetic_fields,
            "temperature": temperature_data,
        }
