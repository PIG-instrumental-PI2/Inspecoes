from typing import List

from models.inspection import InspectionModel, InspectionUpdateModel
from repositories.inspection import InspectionRepository


class InspectionService:
    def __init__(self) -> None:
        self._inspection_repository = InspectionRepository()

    def create(
        self,
        name: str,
        company_id: str,
        pig_id: str,
        place: str,
        description: str = None,
    ) -> InspectionModel:
        inspection_document = InspectionModel(
            name=name,
            company_id=company_id,
            pig_id=pig_id,
            open=True,
            place=place,
            description=description,
        )
        return self._inspection_repository.save(inspection_document)

    def get_all_by_company(self, company_id: str) -> List[InspectionModel]:
        return self._inspection_repository.get_list_by_company(company_id)

    def get_by_id(self, inspection_id: str) -> InspectionModel:
        return self._inspection_repository.get_by_id(inspection_id)

    def close(self, inspection_id: str):
        pass

    def _check_inspection_exists(self, inspection_id: str):
        pass

    # def update(
    #     self,
    #     pig_id: str,
    #     name: str = None,
    #     company: str = None,
    #     description: str = None,
    # ) -> InspectionModel:
    #     pig_changes = InspectionUpdateModel(
    #         id=pig_id, name=name, company_id=company, description=description
    #     )
    #     self._inspection_repository.update(pig_changes)
    #     return self.get_by_id(pig_id)

    # def delete(self, pig_id: str):
    #     self._inspection_repository.delete(pig_id)
