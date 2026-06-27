from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_search_returns_results():
    response = client.post("/search", params={"query": "what is the ELBO"})
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "what is the ELBO"
    assert len(data["results"]) > 0


def test_search_result_has_required_fields():
    response = client.post("/search", params={"query": "test"})
    result = response.json()["results"][0]
    assert "clip_id" in result
    assert "timestamp" in result
    assert "score" in result
