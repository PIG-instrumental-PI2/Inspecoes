import json
from datetime import datetime

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app
from repositories.processed_measurements import ProcessedMeasurementRepository

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/inspections"
INSPECTION_ID = "a43923db765b869af8577c7c"
PIG_ID = "62439cf9f7d653a9088ba15a"
COMPANY_ID = "company-001"
OPENED = True
PLACE = "Station 001 - Complex 001"
CLUSTER_MODEL_ID = "6261851dec992f7e0d8f03f1"


@pytest.fixture()
def inspection_mongo_mock(mocker):
    class MongoResponse:
        def __init__(self, id=INSPECTION_ID) -> None:
            self.inserted_id = ObjectId(id)
            self.upserted_id = ObjectId(id)

    def find_one(self, filter, projection=None):
        collection_name = self.name
        if collection_name == "pigs" and filter == {"_id": ObjectId(PIG_ID)}:
            return {
                "_id": PIG_ID,
                "name": PIG_ID,
                "pig_number": "1234",
                "company_id": COMPANY_ID,
                "description": "",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        if collection_name == "inspections" and filter == {
            "_id": ObjectId(INSPECTION_ID)
        }:
            return {
                "_id": INSPECTION_ID,
                "name": "inspection-001",
                "company_id": COMPANY_ID,
                "pig_id": PIG_ID,
                "open": OPENED,
                "place": PLACE,
                "description": "",
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        if collection_name == "cluster_models":
            return {"_id": CLUSTER_MODEL_ID, "pickled_data": open("./tests/resources/")}
        return None

    mocker.patch(
        "pymongo.collection.Collection.insert_one", return_value=MongoResponse()
    )
    mocker.patch(
        "pymongo.collection.Collection.update_one", return_value=MongoResponse()
    )

    mocker.patch("pymongo.collection.Collection.find_one", find_one)


@pytest.fixture()
def data_mongo_mock(mocker):
    def find(self, filter, projection=None):
        if filter == {"inspection_id": INSPECTION_ID}:
            saved_measurements = json.loads(
                open("./tests/resources/measurements.json", "r").read()
            )
            return saved_measurements
        return None

    mocker.patch("pymongo.collection.Collection.find", find)


def test_success_close_inspection_(mocker, inspection_mongo_mock, data_mongo_mock):
    #### Spies
    save_processed_spy = mocker.spy(ProcessedMeasurementRepository, "save")

    #### Test Request
    response = client.post(f"{API_PATH}/{INSPECTION_ID}/close", headers=HEADERS)
    response_body = response.json()

    #### Assertions
    # Check if 200 measurements are saved (size of data test)
    # save_processed_spy.assert_called()
    assert save_processed_spy.call_count == 200

    assert response.status_code == 201
    assert response_body.get("id") == INSPECTION_ID
    assert response_body.get("open") == False
    assert response_body.get("clusters")


def test_error_close_inspection_inexistent(mocker, inspection_mongo_mock):
    # Test Request
    response = client.post(f"{API_PATH}/inexistent-inspection/close", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 404
    assert response_body == {"error": "Inspeção não encontrada"}
