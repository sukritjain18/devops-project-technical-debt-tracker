from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests

def test_homepage_and_api():
    # Setup Chrome headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    # Test homepage
    driver.get("http://localhost:8080")
    assert "Technical Debt Tracker" in driver.page_source

    # Trigger /api endpoint
    api_resp = requests.get("http://localhost:8080/api")
    api_data = api_resp.json()
    assert api_resp.status_code == 200
    assert api_data["status"] == "ok"

    # Trigger /health endpoint
    health_resp = requests.get("http://localhost:8080/health")
    health_data = health_resp.json()
    assert health_resp.status_code == 200
    assert health_data["status"] == "healthy"

    # Trigger /metrics endpoint
    metrics_resp = requests.get("http://localhost:8080/metrics")
    assert metrics_resp.status_code == 200
    assert "cpu_usage_percent" in metrics_resp.text

    # Trigger /test-email endpoint
    email_resp = requests.get("http://localhost:8080/test-email")
    assert email_resp.status_code == 200
    assert "Email task queued" in email_resp.text  # updated to match new JSON response

    driver.quit()