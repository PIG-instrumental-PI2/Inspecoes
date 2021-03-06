from typing import List, Optional

from fastapi import APIRouter, status

from libraries.crc_utils import CRCUtils
from models.inspection import InspectionModel
from schemas.inspection import InspectionCreationRequest, InspectionDeleteResponse
from services.data_input import DataInputService
from services.inspection import InspectionService
from services.pig import PIGService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=InspectionModel)
def create_inspection(inspection_body: InspectionCreationRequest):
    pig_service = PIGService()
    pig_record = pig_service.get_by_id(pig_id=inspection_body.pig_id)

    inspection_record = InspectionService().create(
        name=inspection_body.name,
        company_id=inspection_body.company_id,
        pig_id=inspection_body.pig_id,
        pig_number=pig_record.pig_number,
        place=inspection_body.place,
        description=inspection_body.description,
    )
    pig_service.update(pig_record.id, current_inspection=inspection_record.id)
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
    "/{inspection_id}/open",
    status_code=status.HTTP_201_CREATED,
    response_model=InspectionModel,
)
def open_inspection(inspection_id: str):
    pig_service = PIGService()

    inspection_record = InspectionService().get_by_id(inspection_id)
    pig_record = pig_service.get_by_id(pig_id=inspection_record.pig_id)
    pig_service.update(pig_record.id, current_inspection=inspection_record.id)
    inspection_record = InspectionService().open(inspection_record)

    return inspection_record


@router.delete(
    "/{inspection_id}",
    status_code=status.HTTP_200_OK,
    response_model=InspectionDeleteResponse,
)
def delete_pig(inspection_id: str):
    InspectionService().delete(inspection_id=inspection_id)
    return InspectionDeleteResponse(id=inspection_id)
