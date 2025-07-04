# src/aurora_platform/schemas/knowledge_schemas.py
from pydantic import BaseModel
from typing import List, Dict, Any

class DocumentCreate(BaseModel):
    doc_text: str
    doc_id: str
    metadata: Dict[str, Any]

class KnowledgeQuery(BaseModel):
    query_text: str
    n_results: int = 3

class SearchResult(BaseModel):
    results: List[str]