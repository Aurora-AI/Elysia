from typing import List

from fastapi import APIRouter, status

from aurora_platform.schemas import cliente_schema
from aurora_platform.services import cliente_service

# Assumindo que o módulo de segurança será criado/ajustado
# from ..core.security import validar_token_firebase

router = APIRouter()

@router.post(
    "/",
    response_model=cliente_schema.Cliente,
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo cliente"
)
async def criar_novo_cliente(
    cliente_data: cliente_schema.ClienteCreate
    # Descomentar quando a segurança estiver implementada
    # usuario_autenticado: dict = Depends(validar_token_firebase)
):
    return cliente_service.create_cliente(cliente_data)

@router.get(
    "/",
    response_model=List[cliente_schema.Cliente],
    summary="Lista todos os clientes"
)
async def listar_clientes(
    # Descomentar quando a segurança estiver implementada
    # usuario_autenticado: dict = Depends(validar_token_firebase)
):
    return cliente_service.get_all_clientes()
