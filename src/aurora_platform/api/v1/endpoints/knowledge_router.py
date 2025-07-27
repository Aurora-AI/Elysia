from fastapi import APIRouter, Depends, HTTPException, status, Request

# --- MUDANÇA: O schema de consulta agora precisa do model_provider ---
from src.aurora_platform.schemas.knowledge_schemas import (
    KnowledgeQuery,
    KnowledgeQueryWithProvider,
    SearchResult,
)
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService

# TODO: Reativar/substituir na integração do Crawler.
# from src.aurora_platform.services.deep_dive_scraper_service import (
# TODO: Reativar/substituir na integração do Crawler.
#     DeepDiveScraperService,
# TODO: Reativar/substituir na integração do Crawler.
# )
from src.aurora_platform.services.rag_service import answer_query

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
    #         text = await scraper.extract_text_from_url(request_body.url)
    #
    #         if not text:
    #             raise HTTPException(
    #                 status_code=400, detail="Não foi possível extrair conteúdo da URL."
    #             )
    #
    #         document_id = f"web_{request_body.url}"
    #         metadata = {"source": request_body.url}
    #
    #         kb_service.add_document(document_id=document_id, text=text, metadata=metadata)
    #         return {"message": f"Conteúdo da URL '{request_body.url}' sendo processado."}
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=500, detail=f"Erro durante a ingestão: {str(e)}"
    #         )
    # TODO: Reativar/substituir na integração do Crawler
    # @router.post("/ingest-from-web", status_code=status.HTTP_202_ACCEPTED)
    # async def ingest_from_web(
    #     request_body: IngestURLRequest,
    #     kb_service: KnowledgeBaseService = Depends(get_kb_service),
    # ):
    #     try:
    #         scraper = DeepDiveScraperService()
    #         text = await scraper.extract_text_from_url(request_body.url)
    #
    #         if not text:
    #             raise HTTPException(
    #                 status_code=400, detail="Não foi possível extrair conteúdo da URL."
    #             )
    #
    #         document_id = f"web_{request_body.url}"
    #         metadata = {"source": request_body.url}
    #
    #         kb_service.add_document(document_id=document_id, text=text, metadata=metadata)
    #         return {"message": f"Conteúdo da URL '{request_body.url}' sendo processado."}
    #     except Exception as e:
    #         raise HTTPException(
    #             status_code=500, detail=f"Erro durante a ingestão: {str(e)}"
    #         )


@router.post("/search", response_model=SearchResult)
async def search_in_kb(
    query: KnowledgeQuery, kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    results = kb_service.retrieve(query=query.query, top_k=query.n_results)
    document_texts = [doc.get("text", "") for doc in results if doc.get("text")]
    return SearchResult(results=document_texts)


@router.post("/ask", summary="Consulta RAG com seleção de modelo")
async def ask_with_rag(request: KnowledgeQueryWithProvider):
    """
    Recebe uma pergunta e o nome do provedor de IA (google, azure, deepseek),
    e retorna uma resposta sintetizada.
    """
    try:
        # Passa a pergunta e o provedor para o serviço RAG
        response = answer_query(
            query=request.query, model_provider=request.model_provider
        )
        return {"answer": response}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorreu um erro ao processar a consulta RAG: {e}",
        )
