import pytest
from fastapi.testclient import TestClient

from main import app

HEADERS = dict()

client = TestClient(app)

API_PATH = "/api/v1/pigs/"
PIG_ID = "62439cf9f7d653a9088ba15a"
COMPANY_ID = "company-001"


@pytest.fixture()
def pig_mongo_mock(mocker):
    def find(self, filter, projection=None):
        if filter == {"company_id": COMPANY_ID}:
            return [
                {
                    "_id": PIG_ID,
                    "name": "pig-001",
                    "pig_number": "1234",
                    "company_id": COMPANY_ID,
                    "description": "",
                }
            ]
        return []

    mocker.patch("pymongo.collection.Collection.find", find)


def test_success_get_pigs(mocker, pig_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}?company_id={COMPANY_ID}", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body[0].get("id") == PIG_ID
    assert response_body[0].get("company_id") == COMPANY_ID


def test_error_get_pigs_empty_pig_list_from_company(mocker, pig_mongo_mock):
    # Test Request
    response = client.get(f"{API_PATH}?company_id=company-002", headers=HEADERS)
    response_body = response.json()

    # Assertions
    assert response.status_code == 200
    assert response_body == []
