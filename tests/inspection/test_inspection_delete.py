import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/inspections"
INSPECTION_ID = "a43923db765b869af8577c7c"


@pytest.fixture()
def inspection_mongo_mock(mocker):
    mocker.patch("pymongo.collection.Collection.delete_one", return_value=None)


def test_success_delete_inspection_(mocker, inspection_mongo_mock):
    # Test Request
    response = client.delete(f"{API_PATH}/{INSPECTION_ID}", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert response_body.get("id") == INSPECTION_ID
    assert response_body.get("status") == "deleted"
