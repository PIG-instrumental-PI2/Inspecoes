from typing import List, Optional

from fastapi import APIRouter, status

from schemas.requests.inspection import InspectionCreationRequest
from schemas.responses.inspection import InspectionResponse
from services.inspection import InspectionService

router = APIRouter()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=InspectionResponse
)
def create_inspection(pig_body: InspectionCreationRequest):
    inspection_record = InspectionService().create(
        name=pig_body.name,
        company_id=pig_body.company_id,
        pig_id=pig_body.pig_id,
        place=pig_body.place,
        description=pig_body.description,
    )
    return InspectionResponse(
        id=inspection_record.id,
        name=inspection_record.name,
        company_id=inspection_record.company_id,
        pig_id=inspection_record.pig_id,
        open=inspection_record.open,
        place=inspection_record.place,
        description=inspection_record.description,
    )


@router.get(
    "/{inspection_id}",
    status_code=status.HTTP_200_OK,
    response_model=InspectionResponse,
)
def get_inspection(inspection_id: str):
    inspection_record = InspectionService().get_by_id(inspection_id)
    return InspectionResponse(
        id=inspection_record.id,
        name=inspection_record.name,
        company_id=inspection_record.company_id,
        pig_id=inspection_record.pig_id,
        open=inspection_record.open,
        place=inspection_record.place,
        description=inspection_record.description,
    )


@router.post(
    "/{inspection_id}/close",
    status_code=status.HTTP_201_CREATED,
    response_model=InspectionResponse,
)
def close_inspection(inspection_id: str):
    inspection_record = InspectionService().close(inspection_id)
    return InspectionResponse(
        id=inspection_record.id,
        name=inspection_record.name,
        company_id=inspection_record.company_id,
        pig_id=inspection_record.pig_id,
        open=inspection_record.open,
        place=inspection_record.place,
        description=inspection_record.description,
    )
