# src/aurora_platform/api/v1/endpoints/knowledge_router.py
from fastapi import APIRouter, Depends, HTTPException
from aurora_platform.schemas.knowledge_schemas import DocumentCreate, KnowledgeQuery, SearchResult
from aurora_platform.services.knowledge_service import KnowledgeBaseService

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Base"]
)

def get_kb_service():
    return KnowledgeBaseService()

@router.post("/documents", status_code=201)
async def add_document_to_kb(
    doc: DocumentCreate,
    kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    try:
        kb_service.add_document(
            doc_text=doc.doc_text,
            doc_id=doc.doc_id,
            metadata=doc.metadata
        )
        return {"message": f"Documento '{doc.doc_id}' adicionado com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {e}")

@router.post("/search", response_model=SearchResult)
async def search_in_kb(
    query: KnowledgeQuery,
    kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    try:
        results = kb_service.search(
            query_text=query.query_text,
            n_results=query.n_results
        )
        return SearchResult(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno: {e}")