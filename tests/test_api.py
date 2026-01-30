from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic shape checks
    assert isinstance(data, dict)
    assert "Tennis Club" in data
    assert "participants" in data["Tennis Club"]


def test_signup_and_remove_participant_flow():
    activity = "Tennis Club"
    test_email = "pytest_user@example.com"

    # Ensure the participant is not already signed up
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    assert test_email not in participants

    # Sign up the participant
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    assert f"Signed up {test_email} for {activity}" in resp.json().get("message", "")

    # Confirm participant is in the list
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert test_email in participants

    # Signing up again should return 400
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 400

    # Remove the participant
    resp = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp.status_code == 200
    assert f"Removed {test_email} from {activity}" in resp.json().get("message", "")

    # Confirm participant is removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert test_email not in participants

    # Deleting again should return 404
    resp = client.delete(f"/activities/{activity}/participants?email={test_email}")
    assert resp.status_code == 404
