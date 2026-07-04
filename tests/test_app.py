from fastapi.testclient import TestClient

from src import app as app_module


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "existing@example.com"
    original_participants = app_module.activities[activity_name]["participants"]
    app_module.activities[activity_name]["participants"] = [email]

    try:
        client = TestClient(app_module.app)

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email},
        )

        # Assert
        assert response.status_code == 400
        assert response.json() == {"detail": "Student already signed up for this activity"}
        assert app_module.activities[activity_name]["participants"] == [email]
    finally:
        app_module.activities[activity_name]["participants"] = original_participants
