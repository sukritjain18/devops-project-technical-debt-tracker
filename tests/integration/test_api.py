from src.app import app, API_KEY

def test_secure_api_authorized():
    client = app.test_client()
    response = client.get("/secure-api", headers={"x-api-key": API_KEY})
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Authorized access"

def test_secure_api_unauthorized():
    client = app.test_client()
    response = client.get("/secure-api", headers={"x-api-key": "wrong-key"})
    assert response.status_code == 401

def test_health_endpoint():
    client = app.test_client()
    resp = client.get("/health")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["status"] == "healthy"

def test_metrics_endpoint():
    client = app.test_client()
    resp = client.get("/metrics")
    assert resp.status_code == 200
    assert b"cpu_usage_percent" in resp.data