from fastapi import APIRouter, File, status
from fastapi.responses import FileResponse, Response, StreamingResponse

from libraries.crc_utils import CRCUtils
from schemas.data_input import CRCResponse
from services.data_input import DataInputService

router = APIRouter()


@router.post("/{pig_id}", status_code=status.HTTP_201_CREATED)
def upload_data(pig_id: str, inspection_data: bytes = File(...)):
    # async def upload_data(pig_id: str, request: Request):
    # inspection_data: bytes = await request.body()
    corrupted_measurements_bytes = b""
    corrupted_measurements = []

    if inspection_data:
        corrupted_measurements = DataInputService().upload_data(
            pig_id=pig_id, encoded_data=inspection_data
        )

    for measurement_pos in corrupted_measurements:
        corrupted_measurements_bytes += CRCUtils.int_to_bytes(measurement_pos, byte_size=2)

    return Response(corrupted_measurements_bytes, status_code=status.HTTP_201_CREATED)
