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
    def find(self, filter, projection=None):
        if filter.get("company_id") == COMPANY_ID or filter.get("pig_id") == PIG_ID:
            return [
                {
                    "_id": INSPECTION_ID,
                    "name": "inspection-001",
                    "company_id": COMPANY_ID,
                    "pig_id": PIG_ID,
                    "open": OPENED,
                    "place": PLACE,
                    "description": "",
                }
            ]
        return []

    mocker.patch("pymongo.collection.Collection.find", find)


def test_success_get_inspections_from_company(mocker, inspection_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}/?company_id={COMPANY_ID}", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0].get("id") == INSPECTION_ID
    assert response_body[0].get("company_id") == COMPANY_ID


def test_success_get_inspections_from_pig(mocker, inspection_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}/?pig_id={PIG_ID}", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0].get("id") == INSPECTION_ID
    assert response_body[0].get("pig_id") == PIG_ID


def test_error_get_inspections_empty_list_from_company(mocker, inspection_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}/?company_id=company-002", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert response_body == []
