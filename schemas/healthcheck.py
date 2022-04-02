from pydantic import BaseModel


################# Responses #################
class HealthCheckResponse(BaseModel):
    status: str
