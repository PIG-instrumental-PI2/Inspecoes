from libraries.mongodb_client import DatabaseClient
from models.measurement import MeasurementModel


class MeasurementRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="measurements")

    def save(self, document: MeasurementModel) -> MeasurementModel:
        self._db_client.save(document.dict(exclude_unset=True), track_time=False)
        return document
