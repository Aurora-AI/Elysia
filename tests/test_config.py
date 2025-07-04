import pytest
from aurora_platform.core.config import settings


def test_settings_exist():
    """Test that settings are loaded"""
    assert hasattr(settings, 'DATABASE_URL')
    assert hasattr(settings, 'SECRET_KEY')
    assert hasattr(settings, 'ALGORITHM')
    assert hasattr(settings, 'ACCESS_TOKEN_EXPIRE_MINUTES')


def test_default_values():
    """Test default configuration values"""
    assert settings.ALGORITHM == "HS256"
    assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
    assert settings.PROJECT_NAME == "Aurora Platform"
    assert settings.PROJECT_VERSION == "1.0.0"


def test_database_url():
    """Test database URL is set"""
    assert settings.DATABASE_URL is not None
    assert len(settings.DATABASE_URL) > 0


def test_secret_key():
    """Test secret key is set"""
    assert settings.SECRET_KEY is not None
    assert len(settings.SECRET_KEY) > 0


def test_allowed_origins():
    """Test CORS allowed origins"""
    assert isinstance(settings.ALLOWED_ORIGINS, list)


def test_optional_settings():
    """Test optional settings have defaults"""
    assert settings.REDIS_URL is None or isinstance(settings.REDIS_URL, str)
    
    