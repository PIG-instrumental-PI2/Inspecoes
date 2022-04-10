from typing import List, Optional

from libraries.mongodb_client import DatabaseClient
from models.measurement import MeasurementModel
from utils.exception_handlers import NotFoundException


class MeasurementRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="measurements")

    def save(self, document: MeasurementModel) -> MeasurementModel:
        document_id = self._db_client.save(document.dict(exclude_unset=True))
        # document.id = document_id
        return document
