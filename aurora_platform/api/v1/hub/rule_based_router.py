from aurora_platform.schemas.etp_schemas import ETPRequest
from aurora_platform.services.etp_generator_service import ETPGeneratorService

from .schemas import HubRequest, HubResponse


class RuleBasedRouter:
    def __init__(self, kb_service):
        self.kb_service = kb_service
        self.rules = {
            "etp": ETPGeneratorService(self.kb_service),
            "estudo técnico preliminar": ETPGeneratorService(self.kb_service),
        }

    async def route(self, request: HubRequest) -> HubResponse:
        task_lower = request.task.lower()
        for keyword, agent in self.rules.items():
            if keyword in task_lower:
                # Chama o agente especialista
                # Espera que o payload seja compatível com ETPRequest
                etp_request = ETPRequest(**request.payload)
                result = await agent.generate_etp(etp_request)
                return HubResponse(result=result, agent=agent.__class__.__name__)
        raise ValueError("No matching agent found for the requested task.")
