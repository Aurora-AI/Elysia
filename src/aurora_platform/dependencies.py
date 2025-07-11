# src/aurora_platform/dependencies.py
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from fastapi import Request

def get_kb_service(request: Request) -> KnowledgeBaseService:
    return request.app.state.kb_service