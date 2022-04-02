from typing import List, Optional

from fastapi import APIRouter, status

from models.inspection import InspectionModel
from schemas.inspection import InspectionCreationRequest
from services.inspection import InspectionService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InspectionModel)
def create_inspection(pig_body: InspectionCreationRequest):
    inspection_record = InspectionService().create(
        name=pig_body.name,
        company_id=pig_body.company_id,
        pig_id=pig_body.pig_id,
        place=pig_body.place,
        description=pig_body.description,
    )
    return inspection_record


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[InspectionModel],
)
def get_inspections(company_id: Optional[str] = None, pig_id: Optional[str] = None):
    inspection_records = InspectionService().get_list_by_filters(company_id, pig_id)
    return inspection_records


@router.get(
    "/{inspection_id}",
    status_code=status.HTTP_200_OK,
    response_model=InspectionModel,
)
def get_inspection(inspection_id: str):
    inspection_record = InspectionService().get_by_id(inspection_id)
    return inspection_record


@router.post(
    "/{inspection_id}/close",
    status_code=status.HTTP_201_CREATED,
    response_model=InspectionModel,
)
def close_inspection(inspection_id: str):
    inspection_record = InspectionService().close(inspection_id)
    return inspection_record
