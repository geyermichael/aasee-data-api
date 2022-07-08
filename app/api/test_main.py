from fastapi.testclient import TestClient
from .main import app

client = TestClient(app)

test_data_result = [{
        "id": 1,
        "datum": "2021-05-18T22:29:00",
        "wassertemperatur": 16.78,
        "ph_wert": 8.32,
        "sauerstoffgehalt": 14.91,
        "aussentemperatur": 8.4
    }]

def test_welcome():
    response = client.get("/")
    assert response.status_code == 200

def test_get_raw_data_by_id():
    response = client.get("/api/v1/raw-data/id/1", json=test_data_result)
    assert response.status_code == 200
    assert response.json() == test_data_result