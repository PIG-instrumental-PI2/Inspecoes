from typing import List, Optional

from pydantic import BaseModel


class InspectionModel(BaseModel):
    id: Optional[str]
    name: str
    company_id: str
    pig_id: str
    open: bool
    place: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    clusters: Optional[List[list]]

    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
        return BaseModel.dict(self, *args, **kwargs)


class InspectionUpdateModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    company_id: Optional[str]
    pig_id: Optional[str]
    place: Optional[str]
    description: Optional[str]
