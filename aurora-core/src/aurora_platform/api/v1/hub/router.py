from fastapi import APIRouter, HTTPException, status

from aurora_platform.services.knowledge_service import KnowledgeBaseService

from .rule_based_router import RuleBasedRouter
from .schemas import HubRequest, HubResponse

router = APIRouter()

# Instancia o servi√ßo de conhecimento e o roteador
kb_service = KnowledgeBaseService()
hub_router = RuleBasedRouter(kb_service=kb_service)


@router.post("/dispatch", response_model=HubResponse)
async def dispatch(request: HubRequest):
    try:
        response = await hub_router.route(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
