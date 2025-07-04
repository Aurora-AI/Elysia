import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from aurora_platform.db.models.user_model import User


def test_login_success(client: TestClient, test_user: User):
    """Test successful login"""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": test_user.email, "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    response = client.post(
        "/api/v1/auth/token",
        data={"username": "invalid@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
    assert "Incorrect username or password" in response.json()["detail"]


# @pytest.mark.asyncio
# async def test_get_current_user(client: TestClient, test_user: User):
#     """Test getting current user info"""
#     # First login to get token
#     login_response = client.post(
#         "/api/v1/auth/token",
#         data={"username": test_user.email, "password": "testpassword"}
#     )
#     token = login_response.json()["access_token"]
#
#     # Then get user info
#     response = client.get(
#         "/api/v1/auth/me",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response.status_code == 200
#     user_data = response.json()
#     assert user_data["email"] == test_user.email
#
# @pytest.mark.asyncio
# async def test_logout(client: TestClient, test_user: User):
#     """Test logout functionality"""
#     # First login
#     login_response = client.post(
#         "/api/v1/auth/token",
#         data={"username": test_user.email, "password": "testpassword"}
#     )
#     token = login_response.json()["access_token"]
#
#     # Then logout
#     response = client.post(
#         "/api/v1/auth/logout",
#         headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response.status_code == 204