from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.api import api_router as api_v1
from schemas.responses.healthcheck import HealthCheckResponse
from utils.exception_handlers import (
    BadRequestException,
    ExceptionHandler,
    InternalServerError,
)

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(Exception, ExceptionHandler.exception_handler)
app.add_exception_handler(BadRequestException, ExceptionHandler.exception_handler)
app.add_exception_handler(InternalServerError, ExceptionHandler.exception_handler)


@app.get("/", response_model=HealthCheckResponse, tags=["HealthCheck"])
def healthcheck():
    return HealthCheckResponse(status="OK")


app.include_router(api_v1, prefix="/api/v1")
