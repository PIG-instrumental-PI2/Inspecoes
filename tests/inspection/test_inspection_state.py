import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/inspections"
INSPECTION_ID = "a43923db765b869af8577c7c"
PIG_ID = "62439cf9f7d653a9088ba15a"
COMPANY_ID = "company-001"
OPENED = True
PLACE = "Station 001 - Complex 001"


@pytest.fixture()
def inspection_mongo_mock(mocker):
    class MongoResponse:
        upserted_id = ObjectId(PIG_ID)

    def find_one(self, filter, projection=None):
        if filter == {"_id": ObjectId(INSPECTION_ID)}:
            return {
                "_id": INSPECTION_ID,
                "name": "inspection-001",
                "company_id": COMPANY_ID,
                "pig_id": PIG_ID,
                "open": OPENED,
                "place": PLACE,
                "description": "",
            }
        return None

    mocker.patch(
        "pymongo.collection.Collection.update_one", return_value=MongoResponse()
    )

    mocker.patch("pymongo.collection.Collection.find_one", find_one)


def test_success_close_inspection_(mocker, inspection_mongo_mock):
    # Test Request
    response = client.post(f"{API_PATH}/{INSPECTION_ID}/close", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 201
    assert response_body.get("id") == INSPECTION_ID
    assert response_body.get("open") == False


def test_success_open_inspection(mocker, inspection_mongo_mock):
    # Test Request
    response = client.post(f"{API_PATH}/{INSPECTION_ID}/open", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 201
    assert response_body.get("id") == INSPECTION_ID
    assert response_body.get("open") == True


def test_error_close_inspection_inexistent(mocker, inspection_mongo_mock):
    # Test Request
    response = client.post(f"{API_PATH}/inexistent-inspection/close", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 404
    assert response_body == {"error": "Resource Not Found"}


def test_error_open_inspection_inexistent(mocker, inspection_mongo_mock):
    # Test Request
    response = client.post(f"{API_PATH}/inexistent-inspection/open", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 404
    assert response_body == {"error": "Resource Not Found"}
