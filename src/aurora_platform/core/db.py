from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .settings import Settings, get_settings

Base = declarative_base()


def make_engine(settings: Settings | None = None):
    settings = settings or get_settings()
    url = settings.DB_URL
    connect_args = {}
    if url.startswith("sqlite"):
        # Necessário para SQLite em thread única (ex.: FastAPI dev)
        connect_args["check_same_thread"] = False
    engine = create_engine(
        url,
        echo=settings.DB_ECHO,
        pool_pre_ping=True,
        connect_args=connect_args,  # OK vazio p/ outros drivers
    )
    return engine


engine = make_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator:
    """
    Gerador de sessão para injeção (compatível com FastAPI):
        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Generator:
    """
    Context manager de sessão, útil para jobs/scripts:
        with session_scope() as db:
            db.add(obj)
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


__all__ = [
    "Base",
    "engine",
    "SessionLocal",
    "get_db",
    "session_scope",
    "make_engine",
]
