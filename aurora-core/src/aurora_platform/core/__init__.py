"""Core package exports used in tests."""
from . import db

# Re-export common test helpers for static analysis
create_db_and_tables = getattr(db, "create_db_and_tables", None)
engine = getattr(db, "engine", None)

__all__ = ["db", "create_db_and_tables", "engine"]
# This file makes src/aurora_platform/core a Python package.
