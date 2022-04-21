from datetime import datetime

import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from libraries.crc_utils import CRCUtils
from main import app
from services.data_input import (
    MAGNETIC_FIELD_SIZE,
    SPEED_SIZE,
    TEMPERATURE_SIZE,
    TIME_SIZE,
)

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/data-input"
INSPECTION_ID = "a43923db765b869af8577c7c"
PIG_ID = "62439cf9f7d653a9088ba15a"
PIG_ID_2 = "8fdf560b3ca5589f7c4af29b"
COMPANY_ID = "company-001"
OPENED = True
PLACE = "Station 001 - Complex 001"

# Inspection Measurement data
INSP_TIME = 1649525795
INSP_SPEED = 1.4
INSP_MAGNETIC_FIELDS = [
    0.22,
    0.56,
    0.16,
    0.08,
    0.53,
    0.55,
    0.18,
    0.78,
    0.6,
    0.9,
    1.02,
    0.45,
    0.36,
    0.47,
    0.21,
    0.83,
]
INSP_TEMPERATURE = 35.7
INSP_PIG_NUMBER = 1


@pytest.fixture()
def data_mongo_mock(mocker):
    class MongoResponse:
        def __init__(self, id=INSPECTION_ID) -> None:
            self.inserted_id = ObjectId(id)
            self.upserted_id = ObjectId(id)

    def find_one(self, filter, projection=None):
        if filter == {"_id": ObjectId(PIG_ID)}:
            return {
                "_id": PIG_ID,
                "name": "pig-001",
                "pig_number": "1234",
                "company_id": COMPANY_ID,
                "description": "",
                "current_inspection": INSPECTION_ID,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        if filter == {"_id": ObjectId(PIG_ID_2)}:
            return {
                "_id": PIG_ID_2,
                "name": "pig-002",
                "pig_number": "1235",
                "company_id": COMPANY_ID,
                "description": "",
                "current_inspection": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
        if filter == {"_id": ObjectId(INSPECTION_ID)}:
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
        return None

    mocker.patch("pymongo.collection.Collection.find_one", find_one)
    mocker.patch(
        "pymongo.collection.Collection.insert_one", return_value=MongoResponse()
    )
    mocker.patch(
        "pymongo.collection.Collection.update_one", return_value=MongoResponse(PIG_ID)
    )


@pytest.fixture()
def measurement_bytes():
    data = CRCUtils.int_to_bytes(INSP_TIME, byte_size=TIME_SIZE)
    data += CRCUtils.float_to_bytes(INSP_SPEED, byte_size=SPEED_SIZE)
    data += b"".join(
        [
            CRCUtils.float_to_bytes(mag, byte_size=MAGNETIC_FIELD_SIZE)
            for mag in INSP_MAGNETIC_FIELDS
        ]
    )
    data += CRCUtils.float_to_bytes(INSP_TEMPERATURE, byte_size=TEMPERATURE_SIZE)
    return data


def test_success_upload_data_1_measurement(mocker, data_mongo_mock, measurement_bytes):
    data = measurement_bytes
    # Calculate CRC
    data = CRCUtils.encode_data(data)

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    assert response_body == b"OK"


def test_success_upload_data_1_measurement_create_another_inspection(
    mocker, data_mongo_mock, measurement_bytes
):
    data = measurement_bytes
    # Calculate CRC
    data = CRCUtils.encode_data(data)

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID_2}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    assert response_body == b"OK"


def test_error_upload_data_1_measurement_1_corrupted(
    mocker, data_mongo_mock, measurement_bytes
):
    data = measurement_bytes
    # Calculate CRC
    data = CRCUtils.encode_data(data)
    # Data corruption
    data = b"E" + data[1:]

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 400
    # medicao 1 com erro
    assert response_body == b"CORRUPTED"


def test_success_upload_data_2_measurements(mocker, data_mongo_mock, measurement_bytes):
    data = measurement_bytes * 2
    # Calculate CRC
    data = CRCUtils.encode_data(data)

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    assert response_body == b"OK"


def test_success_upload_data_100_measurements(
    mocker, data_mongo_mock, measurement_bytes
):
    data = measurement_bytes * 100
    # Calculate CRC
    data = CRCUtils.encode_data(data)

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    assert response_body == b"OK"


def test_error_upload_data_2_measurements_1_corrupted(
    mocker, data_mongo_mock, measurement_bytes
):
    data = measurement_bytes * 2
    # Calculate CRC
    data = CRCUtils.encode_data(data)
    data = b"E" + data[1:]

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 400
    # medicao 1 com erro
    assert response_body == b"CORRUPTED"


def test_success_upload_data_2_measurements_1_corrupted_incomplete_data(
    mocker, data_mongo_mock, measurement_bytes
):
    data = measurement_bytes + b"E"
    # Calculate CRC
    data = CRCUtils.encode_data(data)

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 400
    # medicao 2 com erro
    assert response_body == b"CORRUPTED"


def test_error_upload_data_valid_crc_invalid_data_format(mocker, data_mongo_mock):
    data = b"INVALID_DATA"
    # Calculate CRC
    data = CRCUtils.encode_data(data)

    # Test Request
    inspection_data = {"inspection_data": data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 400
    # medicao 1 com erro
    assert response_body == b"CORRUPTED"
