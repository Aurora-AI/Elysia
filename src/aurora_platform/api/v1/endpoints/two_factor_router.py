from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from aurora_platform.db.database import get_session
from aurora_platform.core.security import get_current_user
from aurora_platform.core.two_factor import generate_2fa_secret, generate_qr_code, verify_2fa_token
from aurora_platform.db.models.user_model import User

router = APIRouter()

@router.post("/setup")
async def setup_2fa(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Setup 2FA for user"""
    if current_user.two_factor_enabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA already enabled"
        )
    
    secret = generate_2fa_secret()
    qr_code = generate_qr_code(current_user.email, secret)
    
    current_user.two_factor_secret = secret
    session.add(current_user)
    session.commit()
    
    return {"qr_code": qr_code, "secret": secret}

@router.post("/verify")
async def verify_2fa(
    token: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Verify and enable 2FA"""
    if not current_user.two_factor_secret:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="2FA not set up"
        )
    
    if not verify_2fa_token(current_user.two_factor_secret, token):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 2FA token"
        )
    
    current_user.two_factor_enabled = True
    session.add(current_user)
    session.commit()
    
    return {"message": "2FA enabled successfully"}