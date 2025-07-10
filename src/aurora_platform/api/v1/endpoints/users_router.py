# src/aurora_platform/api/v1/endpoints/users_router.py

from fastapi import APIRouter, Depends

# --- CORREÇÃO ---
# Removido o prefixo 'src.' das importações para seguir o padrão do projeto.
from aurora_platform.core.security import get_current_user

router = APIRouter()

@router.get("/me")
def read_users_me(
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna os dados do usuário atualmente autenticado.
    """
    return current_user