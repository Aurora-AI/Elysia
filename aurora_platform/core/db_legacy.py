from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# Lazy engine/session creation: avoid importing DB drivers during package import
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/aurora")

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        _engine = create_engine(DATABASE_URL, echo=False, future=True)
    return _engine


def get_sessionmaker():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal


Base = declarative_base()


def SessionLocal():
    """Factory wrapper to get a new Session from the sessionmaker.
    Use like: db = SessionLocal()  # returns a Session instance
    """
    return get_sessionmaker()()
