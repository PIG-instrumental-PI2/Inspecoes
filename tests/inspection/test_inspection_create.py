import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/inspections/"
INSPECTION_ID = "a43923db765b869af8577c7c"
PIG_ID = "62439cf9f7d653a9088ba15a"


@pytest.fixture()
def inspection_mongo_mock(mocker):
    class MongoResponse:
        inserted_id = ObjectId(INSPECTION_ID)

    mocker.patch(
        "pymongo.collection.Collection.insert_one", return_value=MongoResponse()
    )


def test_create_inspection_successfully(mocker, inspection_mongo_mock):
    # Test Request
    request_body = {
        "name": "inspection-001",
        "company_id": "company-001",
        "pig_id": PIG_ID,
        "place": "Station 001 - Complex 001",
        "description": "",
    }
    response = client.post(API_PATH, headers=HEADERS, json=request_body)
    response_body = response.json()

    # Assertions
    assert response.status_code == 201
    assert response_body.get("id") == INSPECTION_ID
    assert response_body.get("name") == "inspection-001"
    assert response_body.get("company_id") == "company-001"
    assert response_body.get("pig_id") == PIG_ID
    assert response_body.get("open") == True
    assert response_body.get("place") == "Station 001 - Complex 001"


def test_create_pig_error_missing_name(mocker, inspection_mongo_mock):
    # Test Request
    request_body = {
        "company_id": "company-001",
        "pig_id": PIG_ID,
        "place": "Station 001 - Complex 001",
        "description": "",
    }
    response = client.post(API_PATH, headers=HEADERS, json=request_body)
    response_body = response.json()

    # Assertions
    assert response.status_code == 422
    assert response_body.get("detail") == [
        {
            "loc": ["body", "name"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


def test_create_pig_error_missing_company(mocker, inspection_mongo_mock):
    # Test Request
    request_body = {
        "name": "inspection-001",
        "pig_id": PIG_ID,
        "place": "Station 001 - Complex 001",
        "description": "",
    }
    response = client.post(API_PATH, headers=HEADERS, json=request_body)
    response_body = response.json()

    # Assertions
    assert response.status_code == 422
    assert response_body.get("detail") == [
        {
            "loc": ["body", "company_id"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


def test_create_pig_error_missing_pig(mocker, inspection_mongo_mock):
    # Test Request
    request_body = {
        "name": "inspection-001",
        "company_id": "company-001",
        "place": "Station 001 - Complex 001",
        "description": "",
    }
    response = client.post(API_PATH, headers=HEADERS, json=request_body)
    response_body = response.json()

    # Assertions
    assert response.status_code == 422
    assert response_body.get("detail") == [
        {
            "loc": ["body", "pig_id"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]
