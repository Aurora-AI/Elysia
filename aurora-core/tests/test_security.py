from src.aurora_platform.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing():
    """Test password hashing and verification"""
    password = "testpassword123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_create_access_token():
    """Test access token creation"""
    data = {"sub": "test@example.com"}
    token = create_access_token(data)
    assert isinstance(token, str)
    assert len(token) > 0


def test_create_refresh_token():
    """Test refresh token creation"""
    data = {"sub": "test@example.com"}
    token = create_refresh_token(data)
    assert isinstance(token, str)
    assert len(token) > 0


def test_authenticate_user_success():
    """Test successful user authentication"""
    user = authenticate_user("admin", "secret")
    assert user is not False
    assert user["username"] == "admin"


def test_authenticate_user_wrong_password():
    """Test authentication with wrong password"""
    user = authenticate_user("admin", "wrongpassword")
    assert user is False


def test_authenticate_user_nonexistent():
    """Test authentication with nonexistent user"""
    user = authenticate_user("nonexistent", "password")
    assert user is False
