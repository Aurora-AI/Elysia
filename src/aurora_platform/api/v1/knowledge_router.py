# src/aurora_platform/api/v1/knowledge_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

# TODO: Importar os serviços quando eles forem criados
# from src.aurora_platform.services.knowledge_service import KnowledgeService

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Base"],
)

class IngestURLRequest(BaseModel):
    """Schema para a requisição de ingestão de URL."""
    url: str

@router.post("/ingest-from-url", status_code=status.HTTP_202_ACCEPTED)
async def ingest_from_url(request: IngestURLRequest):
    """
    Recebe uma URL, dispara o processo de scraping e ingestão em background.
    """
    print(f"INFO: Requisição recebida para ingerir conteúdo da URL: {request.url}")
    
    # TODO: Implementar a chamada assíncrona para os serviços:
    # 1. Chamar o DeepDiveScraperService(url) para obter o conteúdo.
    # 2. Chamar o KnowledgeIngestionService(conteúdo) para processar e salvar no ChromaDB.
    
    return {"message": "Processo de ingestão iniciado. O conteúdo será adicionado à base de conhecimento em breve."}