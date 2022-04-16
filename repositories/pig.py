from datetime import datetime
from typing import List

from libraries.mongodb_client import DatabaseClient
from models.pig import PIGModel
from utils.exception_handlers import NotFoundException


class PIGRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="pigs")

    def save(self, document: PIGModel) -> PIGModel:
        dict_doc = self._db_client.save(document.dict(exclude_unset=True))
        document.id = dict_doc.get("_id")
        document.created_at = datetime.isoformat(dict_doc.get("created_at"))
        document.updated_at = datetime.isoformat(dict_doc.get("updated_at"))
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
                    pig_number=record.get("pig_number"),
                    name=record.get("name"),
                    company_id=record.get("company_id"),
                )
            )
        return records

    def get_by_id(self, pig_id: str) -> PIGModel:
        record = self._db_client.get(query={"_id": pig_id})

        if record:
            try:
                created_at = datetime.isoformat(record.get("created_at"))
            except TypeError:
                created_at = None

            try:
                updated_at = datetime.isoformat(record.get("updated_at"))
            except TypeError:
                updated_at = None

            return PIGModel(
                id=str(record.get("_id")),
                pig_number=record.get("pig_number"),
                name=record.get("name"),
                company_id=record.get("company_id"),
                description=record.get("description"),
                last_inspection=record.get("last_inspection"),
                created_at=created_at,
                updated_at=updated_at,
            )
        else:
            raise NotFoundException("PIG não encontrado")

    def delete(self, pig_id: str):
        self._db_client.delete(query={"_id": pig_id})
