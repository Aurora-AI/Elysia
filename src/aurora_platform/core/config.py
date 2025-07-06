# src/aurora_platform/core/config.py - Sistema Híbrido Dynaconf + Pydantic

from pathlib import Path
from typing import List
from dynaconf import Dynaconf
from pydantic import BaseModel, SecretStr

# Camada de Carregamento: Dynaconf
ROOT_DIR = Path(__file__).parent.parent.parent.parent

dynaconf_settings = Dynaconf(
    root_path=str(ROOT_DIR),
    load_dotenv=True,
    settings_files=[
        "config/settings.toml",
        "config/.secrets.toml"
    ],
    environments=True,
    envvar_prefix="AURORA",
    merge_enabled=True,
)

# Camada de Validação: Pydantic BaseModel
class Settings(BaseModel):
    """
    Modelo Pydantic para validação e type hints das configurações.
    Elimina erros do Pylance fornecendo estrutura estática.
    """
    
    # --- Configurações do Projeto ---
    PROJECT_NAME: str = "Aurora Platform"
    PROJECT_VERSION: str = "0.1.0"
    
    # --- Segredos da Aplicação e Banco de Dados ---
    DATABASE_URL: SecretStr
    SECRET_KEY: SecretStr
    
    # --- Chaves de API de Serviços Externos ---
    GEMINI_API_KEY: SecretStr
    FIRECRAWL_API_KEY: SecretStr
    
    # --- Configurações de Segurança ---
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
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 5
    RATE_LIMIT_PER_MINUTE: int = 20
    
    # --- Configurações do Google Cloud ---
    GOOGLE_CLOUD_PROJECT: str
    GOOGLE_CLOUD_LOCATION: str = "us-central1"
    
    # --- Configurações do Redis ---
    REDIS_URL: str = "redis://localhost:6379/0"

# Camada de Instanciação: Objeto final validado
settings = Settings(**dynaconf_settings.to_dict())