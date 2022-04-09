from pydantic import BaseModel


################# Responses #################
class CRCResponse(BaseModel):
    status: bool
