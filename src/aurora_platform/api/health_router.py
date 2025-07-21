from fastapi import APIRouter, status
from aurora_platform.clients.adapters.redis_adapter import ping as redis_ping
from aurora_platform.clients.adapters.chroma_adapter import heartbeat as chroma_heartbeat

router = APIRouter()

@router.get("/health")
async def health_check():
    services = {
        "redis": redis_ping(),
        "chromadb": chroma_heartbeat()
    }
    healthy = all(services.values())
    return {
        "status": "healthy" if healthy else "unhealthy",
        "services": services
    }, status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
