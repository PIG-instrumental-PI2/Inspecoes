from typing import List

from libraries.crc_utils import CRC_SIZE, CRCUtils
from models.measurement import MeasurementModel
from repositories.measurements import MeasurementRepository

MAGNETIC_FIELDS_AMOUNT = 16
# Sizes in byte
TIME_SIZE = 4
SPEED_SIZE = 4
MAGNETIC_FIELD_SIZE = 4
TEMPERATURE_SIZE = 4
PIG_NUMBER_SIZE = 1
TOTAL_SIZE = (
    TIME_SIZE
    + SPEED_SIZE
    + MAGNETIC_FIELD_SIZE * MAGNETIC_FIELDS_AMOUNT
    + TEMPERATURE_SIZE
    + PIG_NUMBER_SIZE
    + CRC_SIZE
)


class DataInputService:
    def __init__(self) -> None:
        self._measurement_repository = MeasurementRepository()

    def upload_data(self, inspection_id: str, encoded_data: bytes) -> List[int]:
        corrupted_measurements = []

        for index, measurement_bytes in enumerate(self._get_measurements(encoded_data)):
            try:
                data_bytes, crc = CRCUtils.get_data(measurement_bytes)
                if CRCUtils.check_integrity(data_bytes, crc):
                    measurement = self._parse_measurement(data_bytes)
                    self._measurement_repository.save(
                        MeasurementModel(
                            inspection_id=inspection_id,
                            timestamp=measurement.get("time"),
                            speed=measurement.get("speed"),
                            magnetic_fields=measurement.get("magnetic_fields"),
                            temperature=measurement.get("temperature"),
                        )
                    )
                else:
                    raise TypeError()
            except Exception as ex:
                corrupted_measurements.append(index)

        return corrupted_measurements

    def _get_measurements(self, data_bytes: bytes):
        begin = 0
        end = 0
        while True:
            begin = end
            end = begin + TOTAL_SIZE
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
        speed_data = CRCUtils.float_from_bytes(data_bytes[begin_pos:end_pos])

        magnetic_fields = []
        for _ in range(MAGNETIC_FIELDS_AMOUNT):
            begin_pos = end_pos
            end_pos = begin_pos + MAGNETIC_FIELD_SIZE
            magnetic_fields.append(
                CRCUtils.float_from_bytes(data_bytes[begin_pos:end_pos])
            )

        begin_pos = end_pos
        end_pos = begin_pos + TEMPERATURE_SIZE
        temperature_data = CRCUtils.float_from_bytes(data_bytes[begin_pos:end_pos])

        return {
            "time": time_data,
            "speed": speed_data,
            "magnetic_fields": magnetic_fields,
            "temperature": temperature_data,
        }
