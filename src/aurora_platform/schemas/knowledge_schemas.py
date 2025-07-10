# src/aurora_platform/schemas/knowledge_schemas.py

from pydantic import BaseModel
from typing import List, Dict, Any

class DocumentCreate(BaseModel):
    doc_id: str
    doc_text: str
    metadata: Dict[str, Any]

class KnowledgeQuery(BaseModel):
    """Schema para realizar uma busca na base de conhecimento."""
    # --- CORREÇÃO AQUI ---
    query: str
    n_results: int = 3

class SearchResult(BaseModel):
    results: List[str]