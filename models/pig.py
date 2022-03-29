from typing import Optional

from pydantic import BaseModel


class PIGModel(BaseModel):
    id: Optional[str]
    pig_number: str
    name: str
    company_id: str
    description: Optional[str]


class PIGUpdateModel(BaseModel):
    id: Optional[str]
    name: Optional[str]
    company_id: Optional[str]
    description: Optional[str]
