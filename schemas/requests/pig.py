from typing import Optional

from pydantic import BaseModel


class PIGCreationRequest(BaseModel):
    name: str
    pig_number: str
    company_id: str
    description: Optional[str]


class PIGUpdateRequest(BaseModel):
    name: Optional[str]
    company_id: Optional[str]
    description: Optional[str]
