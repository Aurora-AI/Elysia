from sqlmodel import create_engine, SQLModel, Session
from aurora_platform.core.config import settings

# Define the database engine
engine = create_engine(settings.DATABASE_URL, echo=True, future=True)

def create_db_and_tables():
    """Create database tables if they don't exist."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency to get database session."""
    with Session(engine) as session:
        yield session
