from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root_serves_ui():
    response = client.get("/")
    assert response.status_code == 200
    # Root should now be the HTML UI, not JSON
    assert response.headers["content-type"].startswith("text/html")
    # Basic sanity check that we're serving the right page
    assert "Adzuna Job Search" in response.text


def test_health_endpoint_ok():
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "adzuna_job_search"
    assert isinstance(data["adzuna_configured"], bool)
