from fastapi.testclient import TestClient
from FocusedAI.src.main import app

client = TestClient(app)

def test_create_course():
    response = client.post("/courses/", json={"name": "Math"})
    assert response.status_code == 200
    assert response.json()["name"] == "Math"

def test_get_courses():
    response = client.get("/courses/")
    assert response.status_code == 200
    assert len(response.json()) > 0
