# Caminho: src/aurora_platform/core/config.py

from pydantic import SecretStr
# Importe o SettingsConfigDict para configurar o comportamento do Pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Carrega e valida as configurações da aplicação a partir de um arquivo .env.
    """
    # Segredos do Banco de Dados e Aplicação
    DATABASE_URL: SecretStr
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Segredos de APIs Externas
    GEMINI_API_KEY: SecretStr

    # A CORREÇÃO:
    # Configura o Pydantic para ler do arquivo .env e IGNORAR campos extras
    # que ele possa encontrar em outros lugares (como o pyproject.toml).
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'  # <-- Esta linha resolve o erro.
    )

# Cria uma instância única das configurações para ser usada em toda a aplicação
settings = Settings()
