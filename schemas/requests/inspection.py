from typing import Optional

from pydantic import BaseModel


class InspectionCreationRequest(BaseModel):
    name: str
    company_id: str
    pig_id: str
    place: Optional[str]
    description: Optional[str]
