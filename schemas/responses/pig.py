from typing import List, Optional

from pydantic import BaseModel


class PIGResponse(BaseModel):
    id: str
    pig_number: str
    name: str
    company_id: str
    description: Optional[str]


class PIGDeleteResponse(BaseModel):
    id: str
    status = "deleted"
