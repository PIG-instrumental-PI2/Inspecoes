import binascii
from typing import Tuple

CRC_SIZE = 32
BYTES_ENDIANNESS = "big"


class CRCUtils:
    @staticmethod
    def encode_data(data: bytes) -> bytes:
        crc = binascii.crc32(data)
        return data + CRCUtils.int_to_bytes(crc)

    @staticmethod
    def get_data(encoded_data: bytes) -> Tuple[bytes, int]:
        data = encoded_data[:-CRC_SIZE]
        crc = encoded_data[-CRC_SIZE:]
        return data, CRCUtils.int_from_bytes(crc)

    @staticmethod
    def check_integrity(data: bytes, crc: int):
        crc_temp = binascii.crc32(data)
        return crc == crc_temp

    @staticmethod
    def int_to_bytes(x: int) -> bytes:
        return x.to_bytes(CRC_SIZE, BYTES_ENDIANNESS)

    @staticmethod
    def int_from_bytes(xbytes: bytes) -> int:
        return int.from_bytes(xbytes, BYTES_ENDIANNESS)
