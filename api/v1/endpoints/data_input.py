from fastapi import APIRouter, File, status
from fastapi.responses import Response

from models.inspection import InspectionModel
from schemas.data_input import CRCStatusEnum
from services.data_input import DataInputService
from services.inspection import InspectionService
from services.pig import PIGService

router = APIRouter()


@router.post("/{pig_id}", status_code=status.HTTP_201_CREATED)
def upload_data(pig_id: str, inspection_data: bytes = File(...)):
    pig_service = PIGService()
    inspection_service = InspectionService()
    pig_record = pig_service.get_by_id(pig_id=pig_id)

    # Try retrieving the last inspection or create another
    try:
        inspection_record = inspection_service.get_by_id(
            inspection_id=pig_record.current_inspection
        )
    except:
        inspection_record = inspection_service.create(
            name="Nova inspenção (gerada automaticamente)",
            company_id=pig_record.company_id,
            pig_id=pig_record.id,
        )
        pig_service.update(pig_record.id, current_inspection=inspection_record.id)

    if inspection_data:
        corrupted_measurement = DataInputService().upload_data(
            inspection_id=inspection_record.id, encoded_data=inspection_data
        )

    if corrupted_measurement:
        return Response(
            CRCStatusEnum.corrupted,
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    else:
        return Response(
            CRCStatusEnum.ok,
            status_code=status.HTTP_201_CREATED,
        )


@router.post(
    "/{pig_id}/close",
    status_code=status.HTTP_201_CREATED,
    response_model=InspectionModel,
)
def close_inspection(pig_id: str):
    """Closes an inspection and start post processing"""
    pig_service = PIGService()
    data_service = DataInputService()
    inspection_service = InspectionService()

    pig_record = pig_service.get_by_id(pig_id=pig_id)
    inspection_id = pig_record.current_inspection
    inspection_record = inspection_service.get_by_id(inspection_id)
    pig_service.update(pig_record.id, current_inspection=None)
    clusters = data_service.post_processing(inspection_id)
    inspection_record = inspection_service.close(inspection_record, clusters=clusters)

    return inspection_record
