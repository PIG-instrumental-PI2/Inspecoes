from typing import List

from libraries.mongodb_client import DatabaseClient
from models.measurement import ProcessedMeasurementsModel


class ProcessedMeasurementRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="processed_measurements")

    def save(self, document: ProcessedMeasurementsModel) -> ProcessedMeasurementsModel:
        self._db_client.save(document.dict(exclude_unset=True), track_time=False)
        return document

    def get_by_inspection(self, inspection_id: str) -> List[ProcessedMeasurementsModel]:
        records = []
        for record in self._db_client.get_list(query={"inspection_id": inspection_id}):
            records.append(
                ProcessedMeasurementsModel(
                    inspection_id=record.get("inspection_id"),
                    ms_time=record.get("ms_time"),
                    formatted_time=record.get("formatted_time"),
                    position=record.get("position"),
                    temperature=record.get("temperature"),
                    speed=record.get("speed"),
                    magnetic_fields=record.get("magnetic_fields"),
                    magnetic_fields_avg=record.get("magnetic_fields_avg"),
                    clustered_magnetic_fields=record.get("clustered_magnetic_fields"),
                )
            )
        return records
