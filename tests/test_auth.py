from fastapi.testclient import TestClient
from src.aurora_platform.main import app

client = TestClient(app)


def test_login_success():
    """Test successful login"""
    response = client.post(
        "/auth/token", data={"username": "admin", "password": "secret"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    response = client.post(
        "/auth/token", data={"username": "invalid", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


def test_protected_endpoint_without_token():
    """Test accessing protected endpoint without token"""
    response = client.post("/prepare-meeting", json={"client_name": "Test Client"})
    assert response.status_code == 401


def test_protected_endpoint_with_token():
    """Test accessing protected endpoint with valid token"""
    # First login to get token
    login_response = client.post(
        "/auth/token", data={"username": "admin", "password": "secret"}
    )
    token = login_response.json()["access_token"]

    # Then access protected endpoint
    response = client.post(
        "/prepare-meeting",
        json={"client_name": "Test Client"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
