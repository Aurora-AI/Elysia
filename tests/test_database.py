import pytest
from sqlmodel import Session
from aurora_platform.db.database import get_session, create_db_and_tables, engine
from aurora_platform.db.models.user_model import User


def test_get_session():
    """Test database session creation"""
    session_gen = get_session()
    session = next(session_gen)
    assert isinstance(session, Session)
    session.close()


def test_create_db_and_tables():
    """Test database table creation"""
    # This should not raise an exception
    create_db_and_tables()


def test_engine_exists():
    """Test database engine exists"""
    assert engine is not None


def test_user_crud_operations(session: Session):
    """Test basic CRUD operations on User model"""
    # Create
    user = User(
        email="crud@example.com",
        hashed_password="hashed_password",
        full_name="CRUD Test User"
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    
    assert user.id is not None
    
    # Read
    from sqlmodel import select
    found_user = session.exec(select(User).where(User.email == "crud@example.com")).first()
    assert found_user is not None
    assert found_user.email == "crud@example.com"
    
    # Update
    found_user.full_name = "Updated CRUD User"
    session.add(found_user)
    session.commit()
    session.refresh(found_user)
    assert found_user.full_name == "Updated CRUD User"
    
    # Delete
    session.delete(found_user)
    session.commit()
    
    deleted_user = session.exec(select(User).where(User.email == "crud@example.com")).first()
    assert deleted_user is None


def test_user_unique_email_constraint(session: Session):
    """Test that email uniqueness is enforced"""
    user1 = User(
        email="unique@example.com",
        hashed_password="password1"
    )
    user2 = User(
        email="unique@example.com",
        hashed_password="password2"
    )
    
    session.add(user1)
    session.commit()
    
    session.add(user2)
    with pytest.raises(Exception):  # Should raise integrity error
        session.commit()