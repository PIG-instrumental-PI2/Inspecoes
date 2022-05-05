from typing import List

from libraries.mongodb_client import DatabaseClient
from models.measurement import ProcessedMeasurementsModel


class ProcessedMeasurementRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="processed_measurements")

    def save(self, document: ProcessedMeasurementsModel) -> ProcessedMeasurementsModel:
        self._db_client.save(document.dict(exclude_unset=True), track_time=False)
        return document

    def get_by_inspection(
        self, inspection_id: str, start_time: int = None, finish_time: int = None
    ) -> List[ProcessedMeasurementsModel]:
        records = []
        query = {"inspection_id": inspection_id}
        # Time filter example
        # {"ms_time": {"$gte": start_time, "$lte": finish_time}}
        if start_time != None:
            query["ms_time"] = {"$gte": start_time}
        if finish_time != None:
            query_ms_time = query.get("ms_time", dict())
            query_ms_time.update({"$lte": finish_time})

        for record in self._db_client.get_list(query=query):
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
                    clustered_magnetic_fields_avg=record.get(
                        "clustered_magnetic_fields_avg"
                    ),
                )
            )
        records = sorted(records, key=lambda record: record.ms_time)
        return records
