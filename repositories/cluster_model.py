from typing import List

from libraries.mongodb_client import DatabaseClient
from models.cluster_model import ClusterModel


class ClusterModelRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="cluster_models")

    def save(self, document: ClusterModel) -> ClusterModel:
        self._db_client.save(document.dict(exclude_unset=True), track_time=False)
        return document

    def get_by_inspection(self, inspection_id: str) -> List[ClusterModel]:
        records = []
        for record in self._db_client.get_list(query={"inspection_id": inspection_id}):
            records.append(
                ClusterModel(
                    inspection_id=record.get("inspection_id"),
                    pickled_data=record.get("pickled_data"),
                )
            )
        return records
