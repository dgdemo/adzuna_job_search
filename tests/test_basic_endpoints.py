from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Adzuna Job Search API is running"}


def test_health_endpoint_ok():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "adzuna_job_search"
    assert isinstance(data["adzuna_configured"], bool)
