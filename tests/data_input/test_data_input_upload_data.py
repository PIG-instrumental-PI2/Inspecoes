import pytest
from bson.objectid import ObjectId
from fastapi.testclient import TestClient

from libraries.crc_utils import CRCUtils
from main import app
from services.data_input import PIG_NUMBER_SIZE, SPEED_SIZE, TEMPERATURE_SIZE, TIME_SIZE

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
                "last_inspection": INSPECTION_ID,
            }
        if filter == {"_id": ObjectId(PIG_ID_2)}:
            return {
                "_id": PIG_ID_2,
                "name": "pig-002",
                "pig_number": "1235",
                "company_id": COMPANY_ID,
                "description": "",
                "last_inspection": None,
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
def intact_measurement_bytes():
    complete_data = CRCUtils.int_to_bytes(INSP_TIME, byte_size=TIME_SIZE)
    complete_data += CRCUtils.float_to_bytes(INSP_SPEED, byte_size=SPEED_SIZE)
    complete_data += b"".join(
        [CRCUtils.float_to_bytes(mag, byte_size=4) for mag in INSP_MAGNETIC_FIELDS]
    )
    complete_data += CRCUtils.float_to_bytes(
        INSP_TEMPERATURE, byte_size=TEMPERATURE_SIZE
    )
    complete_data += CRCUtils.int_to_bytes(INSP_PIG_NUMBER, byte_size=PIG_NUMBER_SIZE)
    complete_data = CRCUtils.encode_data(complete_data)
    return complete_data


@pytest.fixture()
def corrupted_measurement_bytes():
    complete_data = CRCUtils.int_to_bytes(INSP_TIME, byte_size=TIME_SIZE)
    complete_data += CRCUtils.float_to_bytes(INSP_SPEED, byte_size=SPEED_SIZE)
    complete_data += b"".join(
        [CRCUtils.float_to_bytes(mag, byte_size=4) for mag in INSP_MAGNETIC_FIELDS]
    )
    complete_data += CRCUtils.float_to_bytes(
        INSP_TEMPERATURE, byte_size=TEMPERATURE_SIZE
    )
    complete_data += CRCUtils.int_to_bytes(INSP_PIG_NUMBER, byte_size=PIG_NUMBER_SIZE)
    complete_data = CRCUtils.encode_data(complete_data)
    # Data Change
    complete_data = b"E" + complete_data[1:]
    return complete_data


def test_success_upload_data_1_measurement(
    mocker, data_mongo_mock, intact_measurement_bytes
):
    complete_data = intact_measurement_bytes

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    assert response_body == b""


def test_success_upload_data_1_measurement_create_another_inspection(
    mocker, data_mongo_mock, intact_measurement_bytes
):
    complete_data = intact_measurement_bytes

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID_2}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    assert response_body == b""


def test_success_upload_data_1_measurement_1_corrupted(
    mocker, data_mongo_mock, corrupted_measurement_bytes
):
    complete_data = corrupted_measurement_bytes

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    # medicao 0 com erro
    assert response_body == b"\x00\x00"


def test_success_upload_data_2_measurements_1_corrupted(
    mocker, data_mongo_mock, intact_measurement_bytes, corrupted_measurement_bytes
):
    complete_data = intact_measurement_bytes + corrupted_measurement_bytes

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    # medicao 1 com erro
    assert response_body == b"\x00\x01"


def test_success_upload_data_2_measurements_2_corrupted(
    mocker, data_mongo_mock, intact_measurement_bytes, corrupted_measurement_bytes
):
    complete_data = corrupted_measurement_bytes + corrupted_measurement_bytes

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    # medicao 0 e 1 com erro
    assert response_body == b"\x00\x00\x00\x01"


def test_success_upload_data_3_measurements_2_corrupted(
    mocker, data_mongo_mock, intact_measurement_bytes, corrupted_measurement_bytes
):
    complete_data = (
        corrupted_measurement_bytes
        + intact_measurement_bytes
        + corrupted_measurement_bytes
    )

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    # medicao 0 e 1 com erro
    assert response_body == b"\x00\x00\x00\x02"


def test_success_upload_data_measurement_2_corrupted_incomplete_data(
    mocker, data_mongo_mock, intact_measurement_bytes, corrupted_measurement_bytes
):
    complete_data = corrupted_measurement_bytes + b"E"

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    # medicao 0 e 1 com erro
    assert response_body == b"\x00\x00\x00\x01"


def test_error_upload_data_valid_crc_invalid_data_format(
    mocker, data_mongo_mock, intact_measurement_bytes, corrupted_measurement_bytes
):
    data = b"z"
    encoded = CRCUtils.encode_data(data)
    complete_data = encoded

    # Test Request
    inspection_data = {"inspection_data": complete_data}

    response = client.post(f"{API_PATH}/{PIG_ID}", files=inspection_data)
    response_body = response._content

    # Assertions
    assert response.status_code == 201
    # medicao 0 com erro
    assert response_body == b"\x00\x00"
