# src/aurora_platform/api/v1/endpoints/knowledge_router.py

from fastapi import APIRouter, Depends, HTTPException, status, Request
from src.aurora_platform.schemas.knowledge_schemas import KnowledgeQuery, SearchResult, IngestURLRequest
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService
# --- CORREÇÃO: Importar a CLASSE do serviço de scraping ---
from src.aurora_platform.services.deep_dive_scraper_service import DeepDiveScraperService

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

def get_kb_service(request: Request) -> KnowledgeBaseService:
    """Obtém a instância compartilhada do KnowledgeBaseService."""
    return request.app.state.kb_service

@router.post("/ingest-from-web", status_code=status.HTTP_202_ACCEPTED)
async def ingest_from_web(
    request_body: IngestURLRequest,
    kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    """
    Recebe uma URL, extrai seu conteúdo e ingere na base de conhecimento.
    """
    try:
        # --- CORREÇÃO: Instanciar o serviço e chamar o método correto ---
        scraper = DeepDiveScraperService()
        doc_text = scraper.extract_text_from_url(request_body.url)

        if not doc_text:
            raise HTTPException(status_code=400, detail="Não foi possível extrair conteúdo da URL.")
        
        # --- CORREÇÃO: Usar os nomes de parâmetro corretos ---
        document_id = f"web_{request_body.url}"
        metadata = {"source": request_body.url}
        kb_service.add_document(document_id=document_id, text=doc_text, metadata=metadata)
        
        return {"message": f"Conteúdo da URL '{request_body.url}' sendo processado para ingestão."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a ingestão: {str(e)}")

@router.post("/search", response_model=SearchResult)
async def search_in_kb(
    query: KnowledgeQuery,
    kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    """Realiza uma busca semântica na base de conhecimento."""
    # --- CORREÇÃO: Passar o parâmetro com o nome correto 'top_k' ---
    results = kb_service.retrieve(query=query.query, top_k=query.n_results)
    
    # O método retrieve já formata os resultados, então podemos retorná-los diretamente
    # se o SearchResult for compatível ou ajustar o retorno.
    # Para simplificar, vamos assumir que o SearchResult espera uma lista de textos.
    
    document_texts = [doc.get("text", "") for doc in results]
    return SearchResult(results=document_texts)