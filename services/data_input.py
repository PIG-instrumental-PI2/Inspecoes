from datetime import datetime

from libraries.crc_utils import CRC_SIZE, CRCUtils
from models.measurement import MeasurementModel
from repositories.measurements import MeasurementRepository

MAGNETIC_FIELDS_AMOUNT = 16
# Sizes in byte
TIME_SIZE = 8
SPEED_SIZE = 4
MAGNETIC_FIELD_SIZE = 4
TEMPERATURE_SIZE = 4
READING_SIZE = (
    TIME_SIZE
    + SPEED_SIZE
    + MAGNETIC_FIELD_SIZE * MAGNETIC_FIELDS_AMOUNT
    + TEMPERATURE_SIZE
)


class DataInputService:
    def __init__(self) -> None:
        self._measurement_repository = MeasurementRepository()

    def upload_data(self, inspection_id: str, encoded_data: bytes) -> bool:
        corrupted = False

        try:
            data_bytes, crc = CRCUtils.get_data(encoded_data)
            if CRCUtils.check_integrity(data_bytes, crc):
                for measurement_bytes in self._get_measurements(data_bytes):
                    measurement = self._parse_measurement(measurement_bytes)
                    self._measurement_repository.save(
                        MeasurementModel(
                            inspection_id=inspection_id,
                            timestamp=datetime.utcfromtimestamp(
                                self._convert_uint_timestamp_milis_to_float(
                                    measurement.get("timestamp_milis")
                                )
                            ),
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
            "timestamp_milis": time_data,
            "speed": speed_data,
            "magnetic_fields": magnetic_fields,
            "temperature": temperature_data,
        }

    def _convert_uint_timestamp_milis_to_float(self, timestamp_uint):
        return timestamp_uint / 1000
