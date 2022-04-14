from enum import Enum

from pydantic import BaseModel


class CRCStatusEnum(str, Enum):
    ok = "OK"
    corrupted = "CORRUPTED"


################# Responses #################
class CRCResponse(BaseModel):
    status: CRCStatusEnum
