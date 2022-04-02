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

    mocker.patch("pymongo.collection.Collection.find_one", find_one)


def test_get_inspection_successfully(mocker, inspection_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}/{INSPECTION_ID}/", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert response_body.get("id") == INSPECTION_ID
    assert response_body.get("name") == "inspection-001"
    assert response_body.get("company_id") == COMPANY_ID
    assert response_body.get("pig_id") == PIG_ID
    assert response_body.get("open") == OPENED
    assert response_body.get("place") == PLACE


def test_get_pigs_error_empty_pig_list_from_company(mocker, inspection_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}/inexistent-inspection/", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 404
    assert response_body == {"error": "Resource Not Found"}
