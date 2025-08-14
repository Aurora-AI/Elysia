from fastapi import APIRouter
from aurora_platform.services.etp_service import ETPGeneratorService
# Adicione os schemas Pydantic necessários aqui, ex: from aurora_platform.schemas.etp_schemas import ETPRequest

router = APIRouter()
etp_service = ETPGeneratorService()

@router.post("/generate")
# Substitua 'dict' pelo schema de request quando ele for criado
async def generate_etp_endpoint(request_data: dict):
    # A CORREÇÃO: Chamando o método 'generate_etp' correto do serviço
    return etp_service.generate_etp(request_data)
