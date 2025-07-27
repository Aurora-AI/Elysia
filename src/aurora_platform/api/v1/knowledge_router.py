# src/aurora_platform/api/v1/endpoints/knowledge_router.py

from fastapi import APIRouter, Depends, Request
from aurora_platform.schemas.knowledge_schemas import (
    KnowledgeQuery,
    SearchResult,
)
from aurora_platform.services.knowledge_service import KnowledgeBaseService

# TODO: Reativar/substituir na integração do Crawler.
# from aurora_platform.services.deep_dive_scraper_service import DeepDiveScraperService

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])


def get_kb_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.kb_service


# TODO: Reativar/substituir na integração do Crawler
# @router.post("/ingest-from-web", status_code=status.HTTP_202_ACCEPTED)
# async def ingest_from_web(
#     request_body: IngestURLRequest,
#     kb_service: KnowledgeBaseService = Depends(get_kb_service),
# ):
#     try:
#         scraper = DeepDiveScraperService()
#         doc_text = await scraper.extract_text_from_url(request_body.url)
#
#         if not doc_text:
#             raise HTTPException(
#                 status_code=400, detail="Não foi possível extrair conteúdo da URL."
#             )
#
#         document_id = f"web_{request_body.url}"
#         text = doc_text
#         metadata = {"source": request_body.url}
#
#         kb_service.add_document(document_id=document_id, text=text, metadata=metadata)
#
#         return {
#             "message": f"Conteúdo da URL '{request_body.url}' sendo processado para ingestão."
#         }
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Erro durante a ingestão: {str(e)}"
#         )


@router.post("/search", response_model=SearchResult)
async def search_in_kb(
    query: KnowledgeQuery, kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    results = kb_service.retrieve(query=query.query, top_k=query.n_results)
    document_texts = [doc.get("text", "") for doc in results]
    return SearchResult(results=document_texts)
