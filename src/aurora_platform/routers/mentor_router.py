# src/aurora_platform/routers/mentor_router.py
from fastapi import APIRouter, Body
from pydantic import BaseModel
from src.aurora_platform.services import sales_mentor_service

router = APIRouter()

class MeetingRequest(BaseModel):
    client_name: str

@router.post("/prepare-meeting", response_model=str)
def prepare_meeting_endpoint(request: MeetingRequest):
    """
    Endpoint para receber o nome do cliente e retornar a preparação da reunião.
    """
    advice = sales_mentor_service.prepare_for_meeting(request.client_name)
    return advice