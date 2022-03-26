from typing import List

from models.pig import PIGModel, PIGUpdateModel
from repositories.pig import PIGRepository


class PIGService:
    def __init__(self) -> None:
        self._pig_repository = PIGRepository()

    def create(self, name: str, company: str, description: str = None) -> PIGModel:
        pig_document = PIGModel(name=name, company_id=company, description=description)
        return self._pig_repository.save(pig_document)

    def update(
        self,
        pig_id: str,
        name: str = None,
        company: str = None,
        description: str = None,
    ) -> PIGModel:
        pig_changes = PIGUpdateModel(
            id=pig_id, name=name, company_id=company, description=description
        )
        self._pig_repository.update(pig_changes)
        return self.get_by_id(pig_id)

    def get_by_id(self, pig_id: str) -> PIGModel:
        return self._pig_repository.get_by_id(pig_id)

    def get_all_by_company(self, company: str) -> List[PIGModel]:
        return self._pig_repository.get_list_by_company(company)

    def delete(self, pig_id: str):
        self._pig_repository.delete(pig_id)
