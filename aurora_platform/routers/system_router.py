from fastapi import APIRouter
from ..schemas.harmony_schema import HarmonyMessage

router = APIRouter()


@router.post("/harmony-echo", response_model=HarmonyMessage)
async def harmony_echo(message: HarmonyMessage) -> HarmonyMessage:
    """
    Endpoint de teste que recebe uma mensagem no Formato Harmonia Aurora
    e a retorna, validando a estrutura.
    """
    return message
