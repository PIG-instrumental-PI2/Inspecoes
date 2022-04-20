from fastapi import APIRouter, status

from schemas.charts import ChartsSchema
from services.charts import ChartGroupService

router = APIRouter()


@router.get("/", status_code=status.HTTP_200_OK, response_model=ChartsSchema)
def get_chart(inspection_id: str):
    charts_response = ChartGroupService().get_charts(inspection_id=inspection_id)

    return charts_response
