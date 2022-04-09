import binascii
from typing import Tuple

from libraries.crc_utils import CRCUtils

# from repositories.data_input import DataInputRepository


class DataInputService:
    def __init__(self) -> None:
        # self._inspection_repository = DataInputRepository()
        pass

    def upload_data(self, inspection_id: str, encoded_data: bytes) -> bool:
        data, crc = CRCUtils.get_data(encoded_data)
        return CRCUtils.check_integrity(data, crc)
