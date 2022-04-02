from typing import Optional

from pydantic import BaseModel


################# Requests #################
class InspectionCreationRequest(BaseModel):
    name: str
    company_id: str
    pig_id: str
    place: Optional[str]
    description: Optional[str]


################# Responses #################
class InspectionDeleteResponse(BaseModel):
    id: str
    status = "deleted"
