from fastapi import APIRouter, Depends, HTTPException, status, Request
from aurora_platform.schemas.knowledge_schemas import KnowledgeQuery, SearchResult, IngestURLRequest
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.services.deep_dive_scraper_service import scrape_url

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

def get_kb_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.kb_service

@router.post("/ingest-from-web", status_code=status.HTTP_202_ACCEPTED)
async def ingest_from_web(request_body: IngestURLRequest, kb_service: KnowledgeBaseService = Depends(get_kb_service)):
    try:
        scraped_data = await scrape_url(request_body.url)
        if not scraped_data or 'markdown' not in scraped_data[0]:
            raise HTTPException(status_code=400, detail="Não foi possível extrair conteúdo da URL.")
        page = scraped_data[0]
        document_id = f"web_{page.get('metadata', {}).get('sourceURL', request_body.url)}"
        text = page['markdown']
        metadata = page.get('metadata', {})
        kb_service.add_document(document_id=document_id, text=text, metadata=metadata)
        return {"message": f"Conteúdo da URL '{request_body.url}' sendo processado."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a ingestão: {str(e)}")

@router.post("/search", response_model=SearchResult)
async def search_in_kb(query: KnowledgeQuery, kb_service: KnowledgeBaseService = Depends(get_kb_service)):
    results = kb_service.retrieve(query=query.query, top_k=query.n_results)
    document_texts = [doc.get("text", "") for doc in results]
    return SearchResult(results=document_texts)