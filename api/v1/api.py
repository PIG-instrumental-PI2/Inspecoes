from fastapi import APIRouter

from api.v1.endpoints.charts import router as charts_router
from api.v1.endpoints.data_input import router as data_input_router
from api.v1.endpoints.inspection import router as inspection_router
from api.v1.endpoints.pig import router as pig_router

api_router = APIRouter()

api_router.include_router(pig_router, prefix="/pigs", tags=["PIGs"])
api_router.include_router(
    inspection_router, prefix="/inspections", tags=["Inspections"]
)
api_router.include_router(
    charts_router, prefix="/inspections/{inspection_id}/charts", tags=["Charts"]
)
api_router.include_router(data_input_router, prefix="/data-input", tags=["Data Input"])
