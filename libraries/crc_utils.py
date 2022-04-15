import binascii
import struct
from ctypes import c_int32
from typing import Tuple

import crcmod

# Size in bytes
CRC_SIZE = 2
BYTES_ENDIANNESS = "big"
CRC16_VARIATION = "xmodem"

crcmod.__doc__


class CRCUtils:
    @staticmethod
    def encode_data(data: bytes) -> bytes:
        # crc32 = binascii.crc32(data)
        # crc_value = CRCUtils.int_to_bytes(crc32, 32)
        crc16 = crcmod.predefined.Crc(CRC16_VARIATION)
        crc16.update(data)
        crc_value = CRCUtils.int_to_bytes(crc16.crcValue, CRC_SIZE)
        return data + crc_value

    @staticmethod
    def get_data(encoded_data: bytes) -> Tuple[bytes, int]:
        data = encoded_data[:-CRC_SIZE]
        crc = encoded_data[-CRC_SIZE:]
        crc_len = len(crc)
        return data, CRCUtils.int_from_bytes(crc)

    @staticmethod
    def check_integrity(data: bytes, crc: int):
        # crc32_temp = binascii.crc32(data)
        crc16 = crcmod.predefined.Crc(CRC16_VARIATION)
        crc16.update(data)
        crc16_temp = crc16.crcValue
        return crc == crc16_temp

    @staticmethod
    def int_to_bytes(value: int, byte_size=4, endian=BYTES_ENDIANNESS) -> bytes:
        return value.to_bytes(byte_size, endian)

    @staticmethod
    def int_struct_to_bytes(
        value: int, unsigned=True, byte_size=4, endian=BYTES_ENDIANNESS
    ) -> bytes:
        int_type = "I" if unsigned else "i"
        if endian == "big":
            return bytearray(struct.pack(f">{int_type}", value))[-byte_size:]
        return bytearray(struct.pack(f"<{int_type}", value))[:byte_size]

    @staticmethod
    def int_from_bytes(value: bytes) -> int:
        return int.from_bytes(value, BYTES_ENDIANNESS)

    @staticmethod
    def float_to_bytes(value: float, byte_size=4, endian=BYTES_ENDIANNESS) -> bytes:
        if endian == "big":
            return bytearray(struct.pack(">f", value))[-byte_size:]
        return bytearray(struct.pack("<f", value))[:byte_size]

    @staticmethod
    def float_from_bytes(value: bytes, endian=BYTES_ENDIANNESS) -> float:
        if endian == "big":
            return struct.unpack(">f", value)[0]
        return struct.unpack("<f", value)[0]
