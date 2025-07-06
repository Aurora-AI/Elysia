# src/aurora_platform/core/config.py - Padrão Definitivo com Pydantic-Settings

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    """
    Carrega e valida todas as configurações da aplicação a partir de um arquivo .env
    e/ou variáveis de ambiente.
    Esta classe é a única fonte da verdade para todas as configurações.
    """
    # Configuração para carregar de um arquivo .env e ignorar campos extras.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- Configurações do Projeto ---
    PROJECT_NAME: str = "Aurora Core"
    PROJECT_VERSION: str = "0.1.0"

    # --- Segredos da Aplicação e Banco de Dados (Obrigatórios no .env) ---
    DATABASE_URL: SecretStr
    SECRET_KEY: SecretStr

    # --- Chaves de API de Serviços Externos (Obrigatórias no .env) ---
    GEMINI_API_KEY: SecretStr
    DEEPSEEK_API_KEY: SecretStr
    FIRECRAWL_API_KEY: SecretStr

    # --- Configs de Segurança (com valores padrão do settings.toml) ---
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALLOWED_ORIGINS: List[str] = []
    HTTPS_ONLY: bool = False
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_NUMBERS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True

    # --- Configs de Rate Limiting (com valores padrão do settings.toml) ---
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 5
    RATE_LIMIT_PER_MINUTE: int = 20

    # --- Configs do Google Cloud (Obrigatórias no .env) ---
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str

    # --- Configs do Redis (com valor padrão do settings.toml) ---
    # Opcional para permitir execução sem Redis, se necessário
    REDIS_URL: Optional[str] = "redis://localhost:6379/0"


# Instância única para ser usada em toda a aplicação
# Pylance pode mostrar um aviso aqui sobre argumentos ausentes para os campos
# SecretStr e outros sem valor padrão. Isso é esperado.
# Pydantic-Settings os carrega automaticamente do ambiente ou do arquivo .env
# em tempo de execução.
settings = Settings()  # type: ignore [call-arg]