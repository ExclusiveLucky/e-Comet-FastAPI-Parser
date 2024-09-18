import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_top_100_repos():
    response = client.get("/api/repos/top100")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) <= 100
