# src/aurora_platform/api/routers/etp_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.aurora_platform.schemas.etp_schemas import ETPRequest, ETPResponse, ETPStatus
from src.aurora_platform.core.security import get_current_user
from src.aurora_platform.services.etp_generator_service import ETPGeneratorService
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService
from datetime import datetime
import uuid

router = APIRouter()

def get_kb_service(request: Request) -> KnowledgeBaseService:
    """Obtém a instância compartilhada do KnowledgeBaseService do estado da aplicação."""
    return request.app.state.kb_service

@router.post("/etp/generate", response_model=ETPResponse)
async def generate_etp(
    request: ETPRequest,
    current_user = Depends(get_current_user),
    kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    """
    Gera um ETP baseado nos dados fornecidos usando pipeline RAG.
    Endpoint protegido por autenticação JWT.
    """
    try:
        # Inicializa o serviço de geração de ETP
        etp_service = ETPGeneratorService(kb_service)
        
        # Gera o ETP usando RAG + LLM
        etp_response = await etp_service.generate_etp(request)
        
        # Adiciona informações do usuário aos metadados
        etp_response.metadados["usuario"] = str(current_user)
        etp_response.metadados["versao"] = "2.0"
        
        return etp_response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro na geração do ETP: {str(e)}"
        )

@router.get("/etp/status/{etp_id}", response_model=ETPStatus)
async def get_etp_status(
    etp_id: str,
    current_user = Depends(get_current_user)
):
    """Consulta o status de um ETP específico"""
    return ETPStatus(
        id=etp_id,
        status="concluido",
        progresso=100
    )