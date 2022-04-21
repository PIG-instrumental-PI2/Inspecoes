import pickle
from typing import List, Tuple

import numpy as np
from sklearn.cluster import KMeans

from libraries.crc_utils import CRCUtils
from models.cluster_model import ClusterModel
from models.measurement import MeasurementModel, ProcessedMeasurementsModel
from repositories.cluster_model import ClusterModelRepository
from repositories.measurements import MeasurementRepository
from repositories.processed_measurements import ProcessedMeasurementRepository
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
        self._processed_measurements_repository = ProcessedMeasurementRepository()
        self._cluster_repository = ClusterModelRepository()

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
        """Peform post processing on inspection data and save on database"""
        measurements = self._measurements_repository.get_by_inspection(inspection_id)
        clusters, clustered_fields_by_time = self._clustering(
            inspection_id, measurements
        )
        self._process_and_save_measurements(
            inspection_id=inspection_id,
            measurements=measurements,
            clustered_fields_by_time=clustered_fields_by_time,
        )

        return clusters

    def _clustering(
        self, inspection_id: str, raw_measurements: List[MeasurementModel]
    ) -> Tuple[List[float], dict]:
        # Prepare magnetic fields data
        magnetic_fields_avg = []
        for measurement in raw_measurements:
            magnetic_fields_avg.append(avg(measurement.magnetic_fields))

        magnetic_fields_avg: np.array = np.array(magnetic_fields_avg).reshape(-1, 1)
        kmeans = KMeans(n_clusters=CLUSTERS_COUNT, random_state=42).fit(
            magnetic_fields_avg
        )

        # Save pickle
        pickled_data = pickle.dumps(kmeans)
        self._cluster_repository.save(
            ClusterModel(inspection_id=inspection_id, pickled_data=pickled_data)
        )

        # Make Predictions
        try:
            centers = kmeans.cluster_centers_.tolist()
            centers = list(
                map(
                    lambda center_coordinates: [
                        format_float(cord) for cord in center_coordinates
                    ],
                    centers,
                )
            )
        except:
            centers = []

        try:
            cluster_data = dict()
            for measurement in raw_measurements:
                measurement_fields: np.array = np.array(
                    measurement.magnetic_fields
                ).reshape(-1, 1)
                cluster_data[measurement.ms_time] = kmeans.predict(
                    measurement_fields
                ).tolist()
        except:
            cluster_data = dict()

        return centers, cluster_data

    def _process_and_save_measurements(
        self,
        inspection_id: str,
        measurements: List[MeasurementModel],
        clustered_fields_by_time: dict,
    ):
        current_pos = 0
        measurements_last = len(measurements) - 1

        for index, measurement in enumerate(measurements):
            self._processed_measurements_repository.save(
                ProcessedMeasurementsModel(
                    inspection_id=inspection_id,
                    ms_time=measurement.ms_time,
                    formatted_time=str(
                        HoursTimedelta(microseconds=measurement.ms_time * 1000)
                    ),
                    position=current_pos,
                    temperature=measurement.temperature,
                    speed=measurement.speed,
                    magnetic_fields=measurement.magnetic_fields,
                    magnetic_fields_avg=avg(measurement.magnetic_fields),
                    clustered_magnetic_fields=clustered_fields_by_time.get(
                        measurement.ms_time
                    ),
                )
            )

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
