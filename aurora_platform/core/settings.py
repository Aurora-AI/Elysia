
from __future__ import annotations
from functools import lru_cache
try:
    from pydantic_settings import BaseSettings, SettingsConfigDict
except ImportError:
    from pydantic import BaseSettings  # type: ignore
    SettingsConfigDict = dict  # type: ignore
from pydantic import SecretStr, Field


class Settings(BaseSettings):
    # Ambiente
    ENV: str = Field(default="development")
    TESTING: int = Field(default=0)  # 1 = testes

    # Banco
    DATABASE_URL: SecretStr | None = Field(default=None)
    TEST_DATABASE_URL: SecretStr = Field(default=SecretStr(
        "sqlite+aiosqlite:///:memory:?cache=shared"))

    # Segurança
    SECRET_KEY: SecretStr = Field(default=SecretStr("dev"))

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow",   # <- ignora variáveis extras no .env
    )

    @property
    def database_url(self) -> str:
        """
        Retorna a URL efetiva do banco.
        - Se TESTING=1, usa TEST_DATABASE_URL (sempre definida).
        - Caso contrário, usa DATABASE_URL; se ausente, falha com mensagem clara.
        """
        if int(self.TESTING or 0) == 1:
            return self.TEST_DATABASE_URL.get_secret_value()
        if self.DATABASE_URL is None:
            raise RuntimeError(
                "DATABASE_URL não definida. Configure no .env ou use TESTING=1 para testes."
            )
        return self.DATABASE_URL.get_secret_value()


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


# Instância global que módulos podem importar
settings = get_settings()
