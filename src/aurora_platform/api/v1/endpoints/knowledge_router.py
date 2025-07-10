from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import AsyncGenerator
from aurora_platform.services.openai_service import OpenAIService
from aurora_platform.services.knowledge_service import KnowledgeBaseService

router = APIRouter(prefix="/knowledge", tags=["Knowledge"])

def get_kb_service(): return KnowledgeBaseService()
def get_llm_service(): return OpenAIService()

class KnowledgeQuery(BaseModel):
    query: str

@router.post("/query")
async def query_knowledge(
    query: KnowledgeQuery,
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
    llm_service: OpenAIService = Depends(get_llm_service)
):
    context_docs = kb_service.search(query_text=query.query, n_results=1)
    if not context_docs:
        async def error_stream():
            yield '{"error": "Não encontrei informação relevante na minha base de conhecimento."}'
        return StreamingResponse(error_stream(), media_type="application/json")

    context_text = "\n\n".join(context_docs)
    
    response_generator = llm_service.generate_answer_stream(
        user_question=query.query, context=context_text
    )

    return StreamingResponse(response_generator, media_type="text/event-stream")