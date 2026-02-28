import pytest
from src.app import app

def test_home():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert "Technical Debt Tracker" in response.data.decode()

def test_api():
    client = app.test_client()
    response = client.get("/api")
    assert response.status_code == 200
    assert "API is working" in response.data.decode()