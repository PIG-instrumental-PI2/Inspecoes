from fastapi import APIRouter, File, status
from fastapi.responses import FileResponse, Response, StreamingResponse

from libraries.crc_utils import CRCUtils
from services.data_input import DataInputService
from services.inspection import InspectionService
from services.pig import PIGService

router = APIRouter()


@router.post("/{pig_id}", status_code=status.HTTP_201_CREATED)
def upload_data(pig_id: str, inspection_data: bytes = File(...)):
    # async def upload_data(pig_id: str, request: Request):
    # inspection_data: bytes = await request.body()
    corrupted_measurements_bytes = b""
    corrupted_measurements = []

    pig_service = PIGService()
    inspection_service = InspectionService()
    pig_record = pig_service.get_by_id(pig_id=pig_id)

    # Try retrieving the last inspection or create another
    try:
        inspection_record = inspection_service.get_by_id(
            inspection_id=pig_record.last_inspection
        )
    except:
        inspection_record = inspection_service.create(
            name="Nova inspenção (gerada automaticamente)",
            company_id=pig_record.company_id,
            pig_id=pig_record.id,
        )
        pig_service.update(pig_record.id, last_inspection=inspection_record.id)

    if inspection_data:
        corrupted_measurements = DataInputService().upload_data(
            inspection_id=inspection_record.id, encoded_data=inspection_data
        )

    for measurement_pos in corrupted_measurements:
        corrupted_measurements_bytes += CRCUtils.int_to_bytes(
            measurement_pos, byte_size=2
        )

    return Response(corrupted_measurements_bytes, status_code=status.HTTP_201_CREATED)
