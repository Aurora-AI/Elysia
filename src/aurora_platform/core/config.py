from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security - MAXIMUM LEVEL
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Reduced from 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 1     # Reduced from 7
    
    # Password Security
    MIN_PASSWORD_LENGTH: int = 12
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_NUMBERS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 5
    
    # Security Headers
    SECURE_COOKIES: bool = True
    HTTPS_ONLY: bool = False  # Set to True in production
    
    # AI Services
    GEMINI_API_KEY: str
    GOOGLE_CLOUD_PROJECT: Optional[str] = None
    
    # Project Info
    PROJECT_NAME: str = "Aurora Platform"
    PROJECT_VERSION: str = "1.0.0"
    
    # CORS - RESTRICTED
    ALLOWED_ORIGINS: List[str] = ["https://localhost:3000", "https://aurora.local"]
    
    # Redis (for caching)
    REDIS_URL: Optional[str] = None
    
    # Azure KeyVault (if needed)
    AZURE_KEY_VAULT_URL: Optional[str] = None
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
