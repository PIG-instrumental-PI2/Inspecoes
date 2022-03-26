from typing import List, Optional

from pydantic import BaseModel


class PIGResponse(BaseModel):
    id: str
    name: str
    company_id: str
    description: Optional[str]


class PIGListResponse(BaseModel):
    pigs: List[PIGResponse]


class PIGDeleteResponse(BaseModel):
    id: str
    status = "deleted"
