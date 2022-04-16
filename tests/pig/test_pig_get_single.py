from datetime import datetime

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/pigs"
PIG_ID = "62439cf9f7d653a9088ba15a"
COMPANY_ID = "company-001"


@pytest.fixture()
def pig_mongo_mock(mocker):
    def find_one(self, filter, projection=None):
        if filter == {"_id": ObjectId(PIG_ID)}:
            return {
                "_id": PIG_ID,
                "name": "pig-001",
                "pig_number": "1234",
                "company_id": COMPANY_ID,
                "description": "",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        return None

    mocker.patch("pymongo.collection.Collection.find_one", find_one)


def test_success_get_pig(mocker, pig_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}/{PIG_ID}/", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert response_body.get("id") == PIG_ID
    assert response_body.get("company_id") == COMPANY_ID


def test_error_get_pig_not_found(mocker, pig_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}/inexistent-pig/", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 404
    assert response_body == {"error": "PIG não encontrado"}
