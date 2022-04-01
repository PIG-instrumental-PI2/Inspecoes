from fastapi import APIRouter

from api.v1.endpoints.inspection import router as inspection_router
from api.v1.endpoints.pig import router as pig_router

api_router = APIRouter()

api_router.include_router(pig_router, prefix="/pigs", tags=["PIGs"])
api_router.include_router(
    inspection_router, prefix="/inspections", tags=["Inspections"]
)
