import pytest
from aurora_platform.db.models.user_model import User, UserCreate, UserRead, UserUpdate, Token, TokenData


def test_user_model_creation():
    """Test User model creation"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.is_superuser is False


def test_user_create_schema():
    """Test UserCreate schema"""
    user_data = UserCreate(
        email="test@example.com",
        password="testpassword",
        full_name="Test User"
    )
    assert user_data.email == "test@example.com"
    assert user_data.password == "testpassword"


def test_user_read_schema():
    """Test UserRead schema"""
    user_data = UserRead(
        id=1,
        email="test@example.com",
        full_name="Test User",
        is_active=True,
        is_superuser=False
    )
    assert user_data.id == 1
    assert user_data.email == "test@example.com"


def test_user_update_schema():
    """Test UserUpdate schema"""
    user_data = UserUpdate(
        email="updated@example.com",
        full_name="Updated User"
    )
    assert user_data.email == "updated@example.com"
    assert user_data.full_name == "Updated User"


def test_token_schema():
    """Test Token schema"""
    token = Token(
        access_token="test_token",
        token_type="bearer",
        refresh_token="refresh_token"
    )
    assert token.access_token == "test_token"
    assert token.token_type == "bearer"
    assert token.refresh_token == "refresh_token"


def test_token_data_schema():
    """Test TokenData schema"""
    token_data = TokenData(username="test@example.com")
    assert token_data.username == "test@example.com"


def test_user_defaults():
    """Test User model defaults"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password"
    )
    assert user.is_active is True
    assert user.is_superuser is False
    assert user.full_name is None


def test_user_with_refresh_token():
    """Test User with refresh token"""
    user = User(
        email="test@example.com",
        hashed_password="hashed_password",
        hashed_refresh_token="hashed_refresh_token"
    )
    assert user.hashed_refresh_token == "hashed_refresh_token"