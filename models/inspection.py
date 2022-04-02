from typing import Optional

from pydantic import BaseModel


class InspectionModel(BaseModel):
    id: Optional[str]
    name: str
    company_id: str
    pig_id: str
    open: bool
    place: Optional[str]
    description: Optional[str]


class InspectionUpdateModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    company_id: Optional[str]
    pig_id: Optional[str]
    place: Optional[str]
    description: Optional[str]
