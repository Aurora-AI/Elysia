from __future__ import annotations
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # use SQLite async por padrão; teste não exige Postgres
    database_url: str = "sqlite+aiosqlite:///:memory:"
    # extras
    env: str = "dev"

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
