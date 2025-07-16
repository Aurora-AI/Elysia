"""Router para geração de ETP."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from src.aurora_platform.services.etp_generator_service import ETPGeneratorService, ETPRequest

router = APIRouter(prefix="/etp", tags=["ETP Generator"])

@router.post("/generate", response_class=PlainTextResponse)
async def generate_etp(request: ETPRequest):
    """Gera Estudo Técnico Preliminar baseado em RAG."""
    try:
        generator = ETPGeneratorService()
        etp_document = generator.generate_etp(request)
        return etp_document
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na geração do ETP: {str(e)}")