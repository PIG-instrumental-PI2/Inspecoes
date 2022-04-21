from typing import List

from models.inspection import InspectionModel, InspectionUpdateModel
from repositories.inspection import InspectionRepository
from utils.math_utils import format_float


class InspectionService:
    def __init__(self) -> None:
        self._inspection_repository = InspectionRepository()

    def create(
        self,
        name: str,
        company_id: str,
        pig_id: str,
        place: str = None,
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

    def get_list_by_filters(
        self, company_id: str = None, pig_id: str = None
    ) -> List[InspectionModel]:
        return self._inspection_repository.get_list_by_filters(company_id, pig_id)

    def get_by_id(self, inspection_id: str) -> InspectionModel:
        return self._inspection_repository.get_by_id(inspection_id)

    def close(
        self, inspection: InspectionModel, clusters: List[list] = []
    ) -> InspectionModel:
        inspection.open = False
        inspection.clusters = clusters
        updated_inspection = self._inspection_repository.update(inspection)
        return updated_inspection

    def open(self, inspection: InspectionModel) -> InspectionModel:
        inspection.open = True
        return self._inspection_repository.update(inspection)

    def delete(self, inspection_id: str):
        self._inspection_repository.delete(inspection_id)
