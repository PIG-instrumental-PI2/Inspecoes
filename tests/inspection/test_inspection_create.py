from datetime import datetime

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app
from tests.data_input.test_data_input_upload_data import PIG_ID_2

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/inspections/"
INSPECTION_ID = "a43923db765b869af8577c7c"
PIG_ID = "62439cf9f7d653a9088ba15a"
COMPANY_ID = "company-001"


@pytest.fixture()
def inspection_mongo_mock(mocker):
    class MongoResponse:
        def __init__(self, id=INSPECTION_ID) -> None:
            self.inserted_id = ObjectId(id)
            self.upserted_id = ObjectId(id)

    def find_one(self, filter, projection=None):
        if filter == {"_id": ObjectId(PIG_ID)}:
            return {
                "_id": PIG_ID,
                "name": PIG_ID,
                "pig_number": "1234",
                "company_id": COMPANY_ID,
                "description": "",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        return None

    mocker.patch(
        "pymongo.collection.Collection.insert_one", return_value=MongoResponse()
    )
    mocker.patch(
        "pymongo.collection.Collection.update_one", return_value=MongoResponse(PIG_ID_2)
    )
    mocker.patch("pymongo.collection.Collection.find_one", find_one)


def test_success_create_inspection(mocker, inspection_mongo_mock):
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
    assert response_body.get("created_at")
    assert response_body.get("updated_at")


def test_error_create_pig_missing_name(mocker, inspection_mongo_mock):
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


def test_error_create_pig_missing_company(mocker, inspection_mongo_mock):
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


def test_error_create_pig_missing_pig(mocker, inspection_mongo_mock):
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
