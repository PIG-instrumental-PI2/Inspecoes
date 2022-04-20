from datetime import datetime

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/inspections/{inspection_id}/charts"
INSPECTION_ID = "a43923db765b869af8577c7c"


@pytest.fixture()
def data_mongo_mock(mocker):
    def find_one(self, filter, projection=None):
        if filter == {"_id": ObjectId(INSPECTION_ID)}:
            return {
                "_id": INSPECTION_ID,
                "name": "inspection-001",
                "company_id": "company-001",
                "pig_id": "62439cf9f7d653a9088ba15a",
                "open": True,
                "place": "Station 001 - Complex 001",
                "description": "",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        return None

    def find(self, filter, projection=None):
        return [
            {
                "_id": ObjectId("625b1b5b78c74a4d95fadb2f"),
                "inspection_id": "625b1b5178c74a4d95fad789",
                "ms_time": 184000,
                "speed": 3.7181,
                "magnetic_fields": [
                    2.4939,
                    2.4925,
                    2.4874,
                    2.4900,
                    2.4885,
                    2.4920,
                    2.4962,
                    2.4965,
                    2.5020,
                    2.5104,
                    2.4456,
                    2.4614,
                    2.4616,
                    2.4662,
                    2.4646,
                    2.4723,
                ],
                "temperature": 41.6044,
            }
        ]

    mocker.patch("pymongo.collection.Collection.find", find_one)
    mocker.patch("pymongo.collection.Collection.find", find)


def test_success_get_inspection_charts(mocker, data_mongo_mock):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    response = client.get(api_path)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == 1
    assert response_body.get("temperatures")[0] == 41.6044
    assert response_body.get("speeds")[0] == 3.7181
    assert response_body.get("magnetic_fields_avg")[0] == 2.4826
    assert response_body.get("times")[0] == 184000
