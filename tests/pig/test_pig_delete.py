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
    mocker.patch("pymongo.collection.Collection.delete_one", return_value=None)


def test_delete_pig_successfully(mocker, pig_mongo_mock):
    # Test Request
    response = client.delete(f"{API_PATH}/{PIG_ID}", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert response_body.get("id") == PIG_ID
    assert response_body.get("status") == "deleted"
