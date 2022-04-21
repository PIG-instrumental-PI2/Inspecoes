from datetime import datetime

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from main import app
from utils.date_utils import HoursTimedelta
from utils.math_utils import avg

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/inspections/{inspection_id}/measurements"
INSPECTION_ID = "a43923db765b869af8577c7c"
PIG_ID = "62439cf9f7d653a9088ba15a"
COMPANY_ID = "company-001"
OPENED = True
PLACE = "Station 001 - Complex 001"
CLUSTER_MODEL_ID = "6261851dec992f7e0d8f03f1"
MAGNETIC_FIELDS = [
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
]
CLUSTERED_FIELDS = [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3]
CLUSTERS = [[2.4826], [2.4821], [2.4824], [2.4818], [2.4831]]


@pytest.fixture()
def inspection_mongo_mock(mocker):
    class MongoResponse:
        def __init__(self, id=INSPECTION_ID) -> None:
            self.inserted_id = ObjectId(id)
            self.upserted_id = ObjectId(id)

    def find_one(self, filter, projection=None):
        collection_name = self.name
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
                "clusters": CLUSTERS,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        return None

    mocker.patch("pymongo.collection.Collection.find_one", find_one)


#################### One measurement ####################
@pytest.fixture()
def data_mongo_mock(mocker):
    def find(self, filter, projection=None):
        collection = self.name
        if collection == "processed_measurements":
            return [
                {
                    "_id": ObjectId("625b1b5b78c74a4d95fadb2f"),
                    "inspection_id": "625b1b5178c74a4d95fad789",
                    "ms_time": 184201,
                    "formatted_time": str(HoursTimedelta(microseconds=184201 * 1000)),
                    "speed": 3.7181,
                    "magnetic_fields_avg": avg(MAGNETIC_FIELDS),
                    "magnetic_fields": MAGNETIC_FIELDS,
                    "clustered_magnetic_fields": CLUSTERED_FIELDS,
                    "temperature": 41.6044,
                    "position": 0,
                }
            ]
        return None

    mocker.patch("pymongo.collection.Collection.find", find)


def test_success_get_inspection_charts(mocker, inspection_mongo_mock, data_mongo_mock):
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
    assert response_body.get("times")[0] == 184201
    assert response_body.get("formatted_times")[0] == "00:03:04:201"
    assert response_body.get("clusters") == CLUSTERS
    for field_index in range(16):
        field = response_body.get(f"magnetic_fields_{field_index}")[0]
        clustered_field = response_body.get(f"clustered_magnetic_fields_{field_index}")[
            0
        ]
        assert field == MAGNETIC_FIELDS[field_index]
        assert clustered_field == CLUSTERED_FIELDS[field_index]


#################### 100 measurements ####################
@pytest.fixture()
def data_mongo_mock_100_measurements(mocker):
    def find(self, filter, projection=None):
        measurements = []
        ms_current_time = 184201
        frequency_hz = 5
        period_tick = 1000 / frequency_hz
        for _ in range(100):
            measurements.append(
                {
                    "_id": ObjectId("625b1b5b78c74a4d95fadb2f"),
                    "inspection_id": "625b1b5178c74a4d95fad789",
                    "ms_time": ms_current_time,
                    "formatted_time": str(
                        HoursTimedelta(microseconds=ms_current_time * 1000)
                    ),
                    "speed": 3.7181,
                    "magnetic_fields_avg": avg(MAGNETIC_FIELDS),
                    "magnetic_fields": MAGNETIC_FIELDS,
                    "clustered_magnetic_fields": CLUSTERED_FIELDS,
                    "temperature": 41.6044,
                    "position": 0,
                }
            )
            ms_current_time += period_tick

        return measurements

    mocker.patch("pymongo.collection.Collection.find", find)


def test_success_get_inspection_charts_100_measurements(
    mocker, inspection_mongo_mock, data_mongo_mock_100_measurements
):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    response = client.get(api_path)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == 100
    assert response_body.get("temperatures")[99] == 41.6044
    assert response_body.get("speeds")[99] == 3.7181
    assert response_body.get("magnetic_fields_avg")[99] == 2.4826
    assert response_body.get("times")[99] == 204001
    assert response_body.get("formatted_times")[99] == "00:03:24:001"
    assert response_body.get("clusters") == CLUSTERS
    for field_index in range(16):
        field = response_body.get(f"magnetic_fields_{field_index}")[99]
        clustered_field = response_body.get(f"clustered_magnetic_fields_{field_index}")[
            99
        ]
        assert field == MAGNETIC_FIELDS[field_index]
        assert clustered_field == CLUSTERED_FIELDS[field_index]
