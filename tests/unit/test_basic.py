from src.app import app

def test_home_route():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Technical Debt Tracker" in response.data