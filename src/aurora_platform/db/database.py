from sqlmodel import create_engine, SQLModel
from src.aurora_platform.core.config import settings

# Define the database engine
# The 'echo=True' parameter will log SQL statements, useful for debugging
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

def create_db_and_tables():
    # This function should be called once at application startup
    # to create database tables if they don't exist.
    # For production, Alembic migrations are preferred.
    SQLModel.metadata.create_all(engine)

# SQLModel base class should be defined here or imported if defined elsewhere,
# for Alembic to detect models.
# If you have a central models.py or similar, import SQLModel from there.
# For now, we assume SQLModel itself can be the base for metadata in env.py
# This was already set in alembic/env.py: target_metadata = SQLModel.metadata
# from sqlmodel import SQLModel # This line is already imported above
pass
