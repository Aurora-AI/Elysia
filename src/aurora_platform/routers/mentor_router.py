# GARANTA QUE ESTE ARQUIVO ESTEJA SALVO COM ESTE CONTEÚDO

from fastapi import APIRouter, Depends
from pydantic import BaseModel
# Importa o módulo de serviço
from src.aurora_platform.services import sales_mentor_service
from src.aurora_platform.core.security import get_current_user

router = APIRouter()

class MeetingRequest(BaseModel):
    client_name: str

@router.post("/prepare-meeting", response_model=str, summary="Gera preparação para reunião de vendas")
def prepare_meeting_endpoint(request: MeetingRequest, current_user: dict = Depends(get_current_user)):
    """
    Recebe o nome de um cliente e usa o "Mentor de Vendas de IA"
    para gerar uma análise estratégica e um plano de ação para a reunião.
    """
    # A CHAMADA DA FUNÇÃO DEVE SER EXATAMENTE ESTA
    advice = sales_mentor_service.prepare_for_meeting(client_name=request.client_name)
    return advice