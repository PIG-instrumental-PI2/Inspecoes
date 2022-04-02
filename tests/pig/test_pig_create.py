import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/pigs/"
PIG_ID = "62439cf9f7d653a9088ba15a"


@pytest.fixture()
def pig_mongo_mock(mocker):
    class MongoResponse:
        inserted_id = ObjectId(PIG_ID)

    mocker.patch(
        "pymongo.collection.Collection.insert_one", return_value=MongoResponse()
    )


def test_sucess_create_pig(mocker, pig_mongo_mock):
    # Test Request
    request_body = {
        "name": "pig-001",
        "pig_number": "1234",
        "company_id": "company-001",
        "description": "",
    }
    response = client.post(API_PATH, headers=HEADERS, json=request_body)
    response_body = response.json()

    # Assertions
    assert response.status_code == 201
    assert response_body.get("id") == PIG_ID
    assert response_body.get("name") == "pig-001"
    assert response_body.get("pig_number") == "1234"
    assert response_body.get("company_id") == "company-001"


def test_error_create_pig_missing_name(mocker, pig_mongo_mock):
    # Test Request
    request_body = {
        "pig_number": "1234",
        "company_id": "company-001",
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


def test_error_create_pig_missing_number(mocker, pig_mongo_mock):
    # Test Request
    request_body = {
        "name": "pig-001",
        "company_id": "company-001",
        "description": "",
    }
    response = client.post(API_PATH, headers=HEADERS, json=request_body)
    response_body = response.json()

    # Assertions
    assert response.status_code == 422
    assert response_body.get("detail") == [
        {
            "loc": ["body", "pig_number"],
            "msg": "field required",
            "type": "value_error.missing",
        }
    ]


def test_error_create_pig_missing_company(mocker, pig_mongo_mock):
    # Test Request
    request_body = {
        "name": "pig-001",
        "pig_number": "1234",
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
