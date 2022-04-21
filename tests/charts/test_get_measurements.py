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
                    "temperature": 41.6044,
                    "position": 0,
                }
            ]
        return None

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
    assert response_body.get("magnetic_fields_0")[0] == 2.4939
    assert response_body.get("magnetic_fields_15")[0] == 2.4723
    assert response_body.get("times")[0] == 184201
    assert response_body.get("formatted_times")[0] == "00:03:04:201"


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
                    "temperature": 41.6044,
                    "position": 0,
                }
            )
            ms_current_time += period_tick

        return measurements

    mocker.patch("pymongo.collection.Collection.find", find)


def test_success_get_inspection_charts_100_measurements(
    mocker, data_mongo_mock_100_measurements
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
    assert response_body.get("magnetic_fields_0")[99] == 2.4939
    assert response_body.get("magnetic_fields_15")[99] == 2.4723
    assert response_body.get("times")[99] == 204001
    assert response_body.get("formatted_times")[99] == "00:03:24:001"
