from typing import List, Optional

from libraries.mongodb_client import DatabaseClient
from models.inspection import InspectionModel
from utils.exception_handlers import NotFoundException


class InspectionRepository:
    def __init__(self) -> None:
        self._db_client = DatabaseClient(collection_name="inspections")

    def save(self, document: InspectionModel) -> InspectionModel:
        document_id = self._db_client.save(document.dict(exclude_unset=True))
        document.id = document_id
        return document

    # def update(self, document: InspectionModel) -> InspectionModel:
    #     self._db_client.update(
    #         document.dict(exclude={"id"}, exclude_unset=True, exclude_none=True),
    #         query={"_id": document.id},
    #     )
    #     return document

    # def get_list_by_company(self, company: str) -> List[InspectionModel]:
    #     records = []
    #     for record in self._db_client.get_list(query={"company_id": company}):
    #         records.append(
    #             InspectionModel(
    #                 id=str(record.get("_id")),
    #                 pig_number=record.get("pig_number"),
    #                 name=record.get("name"),
    #                 company_id=record.get("company_id"),
    #                 description=record.get("description"),
    #             )
    #         )
    #     return records

    # def get_by_id(self, pig_id: str) -> InspectionModel:
    #     record = self._db_client.get(query={"_id": pig_id})

    #     if record:
    #         return InspectionModel(
    #             id=str(record.get("_id")),
    #             pig_number=record.get("pig_number"),
    #             name=record.get("name"),
    #             company_id=record.get("company_id"),
    #             description=record.get("description"),
    #         )
    #     else:
    #         raise NotFoundException("Resource Not Found")

    # def delete(self, pig_id: str):
    #     self._db_client.delete(query={"_id": pig_id})
