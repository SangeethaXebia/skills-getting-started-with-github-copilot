from fastapi.testclient import TestClient

from src import app as app_module


def test_duplicate_signup_is_rejected():
    original_participants = app_module.activities["Chess Club"]["participants"]
    app_module.activities["Chess Club"]["participants"] = ["existing@example.com"]

    try:
        client = TestClient(app_module.app)
        response = client.post(
            "/activities/Chess%20Club/signup",
            params={"email": "existing@example.com"},
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Student already signed up"}
        assert app_module.activities["Chess Club"]["participants"] == ["existing@example.com"]
    finally:
        app_module.activities["Chess Club"]["participants"] = original_participants
