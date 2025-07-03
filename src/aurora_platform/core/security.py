from datetime import timedelta, datetime, timezone
from typing import Dict, Optional, Any

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select

from .config import settings
from .jwt_blacklist import is_token_blacklisted
from aurora_platform.db.database import get_session
from aurora_platform.db.models.user_model import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha fornecida corresponde à senha com hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha."""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Cria um novo token de acesso JWT."""
    to_encode = data.copy()
    
    if "type" not in to_encode:
        to_encode["type"] = "access"

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """Cria um novo refresh token JWT."""
    to_encode = data.copy()

    if "type" not in to_encode:
        to_encode["type"] = "refresh"

    expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    expires = datetime.now(timezone.utc) + timedelta(days=expire_days)
    
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)) -> User:
    """Decodifica o token JWT para obter o usuário atual."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Check if token is blacklisted
    if is_token_blacklisted(token):
        raise credentials_exception

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        token_type: Optional[str] = payload.get("type")
        if token_type != "access":
            raise credentials_exception
            
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = db.exec(select(User).where(User.email == username)).first()

    if user is None or not user.is_active:
        raise credentials_exception

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Wrapper para garantir que o usuário obtido do token está ativo."""
    return current_user


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Autentica um usuário, verificando email e senha."""
    user = db.exec(select(User).where(User.email == username)).first()

    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.hashed_password):
        return None

    return user
