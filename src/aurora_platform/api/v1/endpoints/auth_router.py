import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from jose import JWTError

from src.aurora_platform.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_password_hash
)
from src.aurora_platform.core.security import get_current_user, oauth2_scheme

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request
):
    client_ip = request.client.host if request.client else "unknown"
    
    user = authenticate_user(form_data.username, form_data.password)
    
    if not user:
        logger.warning(f"Failed login attempt for {form_data.username} from {client_ip}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})

    logger.info(f"Successful login for {user['username']} from {client_ip}")
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "refresh_token": refresh_token
    }

@router.get("/me")
async def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"username": current_user["username"], "email": current_user.get("email", "")}