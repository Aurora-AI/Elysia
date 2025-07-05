# GARANTA QUE ESTE ARQUIVO ESTEJA SALVO COM ESTE CONTEÚDO

from fastapi import APIRouter
from pydantic import BaseModel
# Importa o módulo de serviço
from src.aurora_platform.services import sales_mentor_service

router = APIRouter()

class MeetingRequest(BaseModel):
    client_name: str

@router.post("/prepare-meeting", response_model=str, summary="Gera preparação para reunião de vendas")
def prepare_meeting_endpoint(request: MeetingRequest):
    """
    Recebe o nome de um cliente e usa o "Mentor de Vendas de IA"
    para gerar uma análise estratégica e um plano de ação para a reunião.
    """
    # A CHAMADA DA FUNÇÃO DEVE SER EXATAMENTE ESTA
    advice = sales_mentor_service.prepare_for_meeting(client_name=request.client_name)
    return advice