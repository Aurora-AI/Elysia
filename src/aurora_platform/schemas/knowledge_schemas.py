# src/aurora_platform/schemas/knowledge_schemas.py

from typing import Any, Dict, List

from pydantic import BaseModel


class DocumentCreate(BaseModel):
    doc_id: str
    doc_text: str
    metadata: Dict[str, Any]


class IngestURLRequest(BaseModel):
    url: str


class KnowledgeQuery(BaseModel):
    """Schema para realizar uma busca na base de conhecimento."""

    query: str
    n_results: int = 3


class KnowledgeQueryWithProvider(BaseModel):
    """Schema para realizar uma consulta RAG com seleção de provedor de LLM."""

    query: str
    model_provider: str  # "google", "azure", ou "deepseek"


class SearchResult(BaseModel):
    results: List[str]
