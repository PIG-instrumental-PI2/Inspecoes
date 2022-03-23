from fastapi import APIRouter

from api.v1.endpoints import pig

api_router = APIRouter()

api_router.include_router(pig.router, prefix="/pigs", tags=["PIG"])
