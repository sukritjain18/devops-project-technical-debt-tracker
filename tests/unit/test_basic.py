from src.app import app, APP_ENV
from unittest.mock import patch

def test_home_route_with_content_and_logging():
    client = app.test_client()

    with patch("src.app.logger") as mock_logger:
        response = client.get("/")

    assert response.status_code == 200

    # Check that environment string is in response
    expected_string = f"Technical Debt Tracker running in {APP_ENV} environment"
    assert expected_string.encode() in response.data

    # verify logger.info was called
    mock_logger.info.assert_called_with("Home endpoint accessed")