from fastapi import APIRouter, status

from schemas.requests.pig import PIGCreationRequest, PIGUpdateRequest
from schemas.responses.pig import PIGDeleteResponse, PIGListResponse, PIGResponse
from services.pig import PIGService

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PIGResponse)
def create_pig(pig_body: PIGCreationRequest):
    pig_record = PIGService().create(
        name=pig_body.name,
        company=pig_body.company_id,
        description=pig_body.description,
    )
    return PIGResponse(
        id=pig_record.id,
        name=pig_record.name,
        company_id=pig_record.company_id,
        description=pig_record.description,
    )


@router.get("/", status_code=status.HTTP_200_OK, response_model=PIGListResponse)
def get_pigs(company_id: str):
    pig_records = PIGService().get_all_by_company(company=company_id)
    pigs_reponse = []
    for pig_record in pig_records:
        pigs_reponse.append(
            PIGResponse(
                id=pig_record.id,
                name=pig_record.name,
                company_id=pig_record.company_id,
                description=pig_record.description,
            )
        )

    return PIGListResponse(pigs=pigs_reponse)


@router.get("/{pig_id}", status_code=status.HTTP_200_OK, response_model=PIGResponse)
def get_pig(pig_id: str):
    pig_record = PIGService().get_by_id(pig_id=pig_id)

    return PIGResponse(
        id=pig_record.id,
        name=pig_record.name,
        company_id=pig_record.company_id,
        description=pig_record.description,
    )


@router.put("/{pig_id}", status_code=status.HTTP_200_OK, response_model=PIGResponse)
def update_pig(pig_id: str, pig_body: PIGUpdateRequest):
    pig_record = PIGService().update(
        pig_id=pig_id,
        name=pig_body.name,
        company=pig_body.company_id,
        description=pig_body.description,
    )

    return PIGResponse(
        id=pig_record.id,
        name=pig_record.name,
        company_id=pig_record.company_id,
        description=pig_record.description,
    )


@router.delete(
    "/{pig_id}", status_code=status.HTTP_200_OK, response_model=PIGDeleteResponse
)
def delete_pig(pig_id: str):
    PIGService().delete(pig_id=pig_id)
    return PIGDeleteResponse(id=pig_id)
