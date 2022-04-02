from typing import List, Optional

from fastapi import APIRouter, status

from models.pig import PIGModel
from schemas.pig import PIGCreationRequest, PIGDeleteResponse, PIGUpdateRequest
from services.pig import PIGService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PIGModel)
def create_pig(pig_body: PIGCreationRequest):
    pig_record = PIGService().create(
        serial_number=pig_body.pig_number,
        name=pig_body.name,
        company=pig_body.company_id,
        description=pig_body.description,
    )
    return pig_record


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[PIGModel])
def get_pigs(company_id: str):
    pig_records = PIGService().get_all_by_company(company=company_id)
    return pig_records


@router.get("/{pig_id}", status_code=status.HTTP_200_OK, response_model=PIGModel)
def get_pig(pig_id: str):
    pig_record = PIGService().get_by_id(pig_id=pig_id)
    return pig_record


@router.put("/{pig_id}", status_code=status.HTTP_200_OK, response_model=PIGModel)
def update_pig(pig_id: str, pig_body: PIGUpdateRequest):
    pig_record = PIGService().update(
        pig_id=pig_id,
        name=pig_body.name,
        company=pig_body.company_id,
        description=pig_body.description,
    )
    return pig_record


@router.delete(
    "/{pig_id}", status_code=status.HTTP_200_OK, response_model=PIGDeleteResponse
)
def delete_pig(pig_id: str):
    PIGService().delete(pig_id=pig_id)
    return PIGDeleteResponse(id=pig_id)
