from src.app import app

def test_api_endpoint():
    client = app.test_client()
    response = client.get("/api")

    data = response.get_json()

    assert response.status_code == 200
    assert data["status"] == "ok"


def test_api_response_structure():
    client = app.test_client()
    response = client.get("/api")

    data = response.get_json()

    assert "status" in data
    assert "message" in data