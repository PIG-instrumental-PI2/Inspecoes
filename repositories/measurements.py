from typing import List

from libraries.mongodb_client import DatabaseClient
from models.measurement import MeasurementModel


class MeasurementRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="measurements")

    def save(self, document: MeasurementModel) -> MeasurementModel:
        self._db_client.save(document.dict(exclude_unset=True), track_time=False)
        return document

    def get_by_inspection(self, inspection_id: str) -> List[MeasurementModel]:
        records = []
        for record in self._db_client.get_list(query={"inspection_id": inspection_id}):
            records.append(
                MeasurementModel(
                    inspection_id=record.get("inspection_id"),
                    ms_time=record.get("ms_time"),
                    speed=record.get("speed"),
                    magnetic_fields=record.get("magnetic_fields"),
                    temperature=record.get("temperature"),
                )
            )
        return records
