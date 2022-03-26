from pydantic import BaseModel


class PIGCreationRequest(BaseModel):
    name: str
