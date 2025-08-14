<<<<<<< HEAD
=======

>>>>>>> origin/main
from fastapi import APIRouter, BackgroundTasks, Depends

from aurora_platform.dependencies import get_kb_service
from aurora_platform.services.knowledge_service import KnowledgeBaseService

router = APIRouter()

<<<<<<< HEAD

=======
>>>>>>> origin/main
@router.get("/health", tags=["Health"])
async def health_check(
    background_tasks: BackgroundTasks,
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """
    Retorna um status imediato e dispara uma verificação de saúde
    dos serviços dependentes em background.
    """
    background_tasks.add_task(kb_service.verify_connection_health)
    return {"status": "Health check initiated"}
