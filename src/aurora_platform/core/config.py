# Caminho: src/aurora_platform/core/config.py

from pydantic import SecretStr
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Carrega e valida as configurações da aplicação a partir de um arquivo .env.
    """
    # Define a fonte das configurações (.env) e o comportamento
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    # Configurações do Projeto
    PROJECT_NAME: str = "Aurora Platform"
    PROJECT_VERSION: str = "0.1.0"
    
    # Segredos do Banco de Dados e Aplicação
    DATABASE_URL: SecretStr
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- INÍCIO DA ADIÇÃO ---
    # Configurações do Google Cloud
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str
    # --- FIM DA ADIÇÃO ---

    # Segredos de APIs Externas
    GEMINI_API_KEY: SecretStr

    # Configurações de Segurança
    ALLOWED_ORIGINS: List[str] = []
    HTTPS_ONLY: bool = False
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_NUMBERS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 5
    RATE_LIMIT_PER_MINUTE: int = 20

    # Configurações do Redis
    REDIS_URL: str = "redis://localhost:6379/0"


# Cria uma instância única das configurações para ser usada em toda a aplicação
# O Pylance pode relatar um erro aqui por não conseguir inferir estaticamente
# que as variáveis de ambiente serão carregadas. Sabemos que o Pydantic
# cuidará disso em tempo de execução, então podemos ignorar o aviso.
settings = Settings()  # type: ignore