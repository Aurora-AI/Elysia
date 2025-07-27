from fastapi import APIRouter, Depends, BackgroundTasks
from src.aurora_platform.dependencies import get_kb_service
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService

router = APIRouter()

@router.get("/health", tags=["Health"])
async def health_check(
    background_tasks: BackgroundTasks,
    kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    """
    Retorna um status imediato e dispara uma verificação de saúde
    dos serviços dependentes em background.
    """
    background_tasks.add_task(kb_service.verify_connection_health)
    return {"status": "Health check initiated"}
from fastapi import APIRouter, status
from aurora_platform.clients.adapters.redis_adapter import ping as redis_ping
from aurora_platform.clients.adapters.chroma_adapter import (
    heartbeat as chroma_heartbeat,
)

router = APIRouter()


@router.get("/health")
async def health_check():
    services = {"redis": redis_ping(), "chromadb": chroma_heartbeat()}
    healthy = all(services.values())
    return {"status": "healthy" if healthy else "unhealthy", "services": services}, (
        status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    )
