import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlmodel import Session, select
from jose import JWTError

from aurora_platform.db.database import get_session
from aurora_platform.core import security
from aurora_platform.core.security_logger import log_login_attempt
from aurora_platform.core.input_validator import validate_user_input
from aurora_platform.db.models.user_model import User, Token

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request,
    session: Session = Depends(get_session)
):
    client_ip = request.client.host if request.client else "unknown"
    
    # Input validation
    validate_user_input(email=form_data.username, password=form_data.password)
    
    user = security.authenticate_user(
        session, username=form_data.username, password=form_data.password
    )
    
    if not user:
        log_login_attempt(form_data.username, False, client_ip)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = security.create_access_token(
        data={"sub": user.email}
    )
    refresh_token = security.create_refresh_token(
        data={"sub": user.email}
    )

    # Store hashed refresh token in the database
    user.hashed_refresh_token = security.get_password_hash(refresh_token)
    session.add(user)
    session.commit()
    session.refresh(user)

    log_login_attempt(user.email, True, client_ip)
    
    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: User = Depends(security.get_current_user),
    session: Session = Depends(get_session)
):
    # Clear the refresh token from the database
    current_user.hashed_refresh_token = None
    session.add(current_user)
    session.commit()
    return

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: Annotated[str, Depends(security.oauth2_scheme)],
    request: Request,
    session: Session = Depends(get_session)
):
    client_ip = request.client.host if request.client else "unknown"
    
    # Validate refresh token and get user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        from jose import jwt
        from aurora_platform.core.config import settings
        
        payload = jwt.decode(refresh_token, settings.SECRET_KEY.get_secret_value(), algorithms=[settings.ALGORITHM])
        token_type = payload.get("type")
        if token_type != "refresh":
            raise credentials_exception
            
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception

    user = session.exec(select(User).where(User.email == username)).first()
    if user is None or not user.is_active:
        raise credentials_exception

    # Generate new tokens
    new_access_token = security.create_access_token(data={"sub": user.email})
    new_refresh_token = security.create_refresh_token(data={"sub": user.email})

    # Store the new hashed refresh token
    user.hashed_refresh_token = security.get_password_hash(new_refresh_token)
    session.add(user)
    session.commit()
    session.refresh(user)

    logger.info(f"Token refreshed for user: {user.email} from IP: {client_ip}")

    return {"access_token": new_access_token, "token_type": "bearer", "refresh_token": new_refresh_token}

@router.get("/me")
async def read_users_me(
    current_user: User = Depends(security.get_current_user)
):
    user_data = current_user.model_dump()
    user_data.pop("hashed_password", None)
    user_data.pop("hashed_refresh_token", None)
    return user_data
