from fastapi import APIRouter
from fastapi import status

from schemas.requests.pig import PIGCreationRequest
from schemas.responses.pig import PIGRecordResponse

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PIGRecordResponse)
async def create_pig(pig_body: PIGCreationRequest):
    return PIGRecordResponse(name=pig_body.name)
