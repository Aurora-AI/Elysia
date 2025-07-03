import pytest
from aurora_platform.core.security import (
    verify_password, 
    get_password_hash, 
    create_access_token, 
    create_refresh_token,
    authenticate_user
)
from aurora_platform.db.models.user_model import User
from sqlmodel import Session


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


def test_authenticate_user_success(session: Session, test_user: User):
    """Test successful user authentication"""
    user = authenticate_user(session, test_user.email, "testpassword")
    assert user is not None
    assert user.email == test_user.email


def test_authenticate_user_wrong_password(session: Session, test_user: User):
    """Test authentication with wrong password"""
    user = authenticate_user(session, test_user.email, "wrongpassword")
    assert user is None


def test_authenticate_user_nonexistent(session: Session):
    """Test authentication with nonexistent user"""
    user = authenticate_user(session, "nonexistent@example.com", "password")
    assert user is None


def test_authenticate_inactive_user(session: Session):
    """Test authentication with inactive user"""
    from aurora_platform.core.security import get_password_hash
    
    inactive_user = User(
        email="inactive@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=False
    )
    session.add(inactive_user)
    session.commit()
    
    user = authenticate_user(session, "inactive@example.com", "testpassword")
    assert user is None