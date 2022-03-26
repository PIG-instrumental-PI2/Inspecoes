from typing import List

from libraries.mongodb_client import DatabaseClient
from models.pig import PIGModel


class PIGRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="pigs")

    def save(self, document: PIGModel) -> PIGModel:
        document_id = self._db_client.save(document.dict(exclude_unset=True))
        document.id = document_id
        return document

    def update(self, document: PIGModel) -> PIGModel:
        self._db_client.update(
            document.dict(exclude={"id"}, exclude_unset=True, exclude_none=True),
            query={"_id": document.id},
        )
        return document

    def get_list_by_company(self, company: str) -> List[PIGModel]:
        records = []
        for record in self._db_client.get_list(query={"company_id": company}):
            records.append(
                PIGModel(
                    id=str(record.get("_id")),
                    name=record.get("name"),
                    company_id=record.get("company_id"),
                    description=record.get("description"),
                )
            )
        return records

    def get_by_id(self, pig_id: str) -> PIGModel:
        record = self._db_client.get(query={"_id": pig_id})

        return PIGModel(
            id=str(record.get("_id")),
            name=record.get("name"),
            company_id=record.get("company_id"),
            description=record.get("description"),
        )

    def delete(self, pig_id: str):
        self._db_client.delete(query={"_id": pig_id})
