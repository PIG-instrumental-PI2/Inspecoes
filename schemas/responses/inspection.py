from typing import List, Optional

from pydantic import BaseModel


class InspectionResponse(BaseModel):
    id: str
    name: str
    company_id: str
    pig_id: str
    open: bool
    place: str
    description: Optional[str]
