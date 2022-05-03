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
CLUSTERED_AVG_FIELD = 3
CLUSTERS = [[2.4826], [2.4821], [2.4824], [2.4818], [2.4831]]
MIN_TIME = 184201
MEASUREMENTS_FREQUENCY = 5
MEASUREMENTS_PERIOD = 1000 / MEASUREMENTS_FREQUENCY
MEASUREMENTS_COUNT = 100
MAX_TIME = int(MIN_TIME + (MEASUREMENTS_PERIOD * (MEASUREMENTS_COUNT - 1)))  # 204001


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
                    "ms_time": MIN_TIME,
                    "formatted_time": str(HoursTimedelta(microseconds=MIN_TIME * 1000)),
                    "speed": 3.7181,
                    "magnetic_fields_avg": avg(MAGNETIC_FIELDS),
                    "magnetic_fields": MAGNETIC_FIELDS,
                    "clustered_magnetic_avg": CLUSTERED_AVG_FIELD,
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
    assert response_body.get("times")[0] == MIN_TIME
    assert response_body.get("formatted_times")[0] == "00:03:04:201"
    assert response_body.get("clusters") == CLUSTERS
    assert response_body.get("clustered_magnetic_avg")[0] == CLUSTERED_AVG_FIELD


#################### Test several measurements ####################
@pytest.fixture()
def data_mongo_mock_several_measurements(mocker):
    def find(self, filter, projection=None):
        measurements = []
        ms_current_time = MIN_TIME
        records_count = MEASUREMENTS_COUNT
        # Time filter example
        # {"ms_time": {"$gte": start_time, "$lte": finish_time}}
        start_time = filter.get("ms_time", dict()).get("$gte", MIN_TIME)
        finish_time = filter.get("ms_time", dict()).get("$lte", MAX_TIME)

        while (
            records_count
            and ms_current_time >= start_time
            and ms_current_time <= finish_time
        ):
            records_count -= 1
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
                    "clustered_magnetic_avg": CLUSTERED_AVG_FIELD,
                    "temperature": 41.6044,
                    "position": 0,
                }
            )
            ms_current_time += MEASUREMENTS_PERIOD

        return measurements

    mocker.patch("pymongo.collection.Collection.find", find)


#################### Tests with time filters ####################
def test_success_get_inspection_charts_100_measurements(
    mocker, inspection_mongo_mock, data_mongo_mock_several_measurements
):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    response = client.get(api_path)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == MEASUREMENTS_COUNT
    assert response_body.get("temperatures")[99] == 41.6044
    assert response_body.get("speeds")[99] == 3.7181
    assert response_body.get("magnetic_fields_avg")[99] == 2.4826
    assert response_body.get("times")[99] == MAX_TIME
    assert response_body.get("formatted_times")[99] == "00:03:24:001"
    assert response_body.get("clusters") == CLUSTERS
    assert response_body.get("clustered_magnetic_avg")[99] == CLUSTERED_AVG_FIELD


def test_success_get_inspection_charts_100_measurements_time_filtered_complete_list(
    mocker, inspection_mongo_mock, data_mongo_mock_several_measurements
):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    response = client.get(f"{api_path}?start_time={MIN_TIME}&finish_time={MAX_TIME}")
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == MEASUREMENTS_COUNT


def test_success_get_inspection_charts_100_measurements_time_filtered_one_measurement(
    mocker, inspection_mongo_mock, data_mongo_mock_several_measurements
):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    response = client.get(f"{api_path}?start_time={MIN_TIME}&finish_time={MIN_TIME}")
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == 1


def test_success_get_inspection_charts_100_measurements_time_filtered_half_measurements(
    mocker, inspection_mongo_mock, data_mongo_mock_several_measurements
):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    fiftieth_measurement_time = int(MIN_TIME + (MEASUREMENTS_PERIOD * 50 - 1))
    response = client.get(
        f"{api_path}?start_time={MIN_TIME}&finish_time={fiftieth_measurement_time}"
    )
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == 50


def test_success_get_inspection_charts_100_measurements_time_filtered_without_start_time(
    mocker, inspection_mongo_mock, data_mongo_mock_several_measurements
):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    fiftieth_measurement_time = int(MIN_TIME + (MEASUREMENTS_PERIOD * 50 - 1))
    response = client.get(f"{api_path}?finish_time={MAX_TIME}")
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == MEASUREMENTS_COUNT


def test_success_get_inspection_charts_100_measurements_time_filtered_without_finish_time(
    mocker, inspection_mongo_mock, data_mongo_mock_several_measurements
):
    # Test Request
    api_path = API_PATH.format(inspection_id=INSPECTION_ID)
    fiftieth_measurement_time = int(MIN_TIME + (MEASUREMENTS_PERIOD * 50 - 1))
    response = client.get(f"{api_path}?start_time={MIN_TIME}")
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body.get("temperatures")) == MEASUREMENTS_COUNT
