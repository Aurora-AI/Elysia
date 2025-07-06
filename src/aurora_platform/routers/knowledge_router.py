# src/aurora_platform/routers/knowledge_router.py
import os
import shutil
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.aurora_platform.services.deep_dive_scraper_service import scrape_and_save_url
from src.aurora_platform.services.knowledge_ingestion_service import ingest_documents
from src.aurora_platform.services.rag_service import answer_query

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

class URLRequest(BaseModel):
    url: str

class QueryRequest(BaseModel):
    query: str

@router.post("/ingest-from-url")
async def ingest_from_url(request: URLRequest):
    """Ingere conhecimento a partir de uma URL usando scraping e ingestão."""
    temp_dir = "./temp_ingestion_data"
    
    try:
        # Scraping da URL e salvamento em arquivo
        await scrape_and_save_url(request.url, temp_dir)
        
        # Ingestão dos documentos
        ingest_documents(temp_dir)
        
        # Limpeza do diretório temporário
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        return {
            "status": "success", 
            "message": "Conhecimento da URL foi assimilado com sucesso pela Memória Ativa."
        }
        
    except Exception as e:
        # Limpeza em caso de erro
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        
        raise HTTPException(
            status_code=500, 
            detail=f"Erro durante a ingestão: {str(e)}"
        )

@router.post("/query")
async def query_knowledge(request: QueryRequest):
    """Responde a uma pergunta usando RAG com a Memória Ativa."""
    try:
        answer = await answer_query(request.query)
        return {"answer": answer}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar consulta: {str(e)}"
        )