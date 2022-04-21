from fastapi import APIRouter, status

from schemas.charts import ChartsSchema
from services.charts import ChartGroupService
from services.inspection import InspectionService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=ChartsSchema)
def get_measurements(inspection_id: str):
    inspection_service = InspectionService()
    charts_service = ChartGroupService()

    inspection_record = inspection_service.get_by_id(inspection_id)
    charts_response = charts_service.get_measurements(inspection_id=inspection_id)
    charts_response.clusters = inspection_record.clusters

    return charts_response
