from fastapi import APIRouter

router = APIRouter()

@router.get("/sentry-debug")
async def trigger_error():
    # Esta rota intencionalmente causa um erro para testar o Sentry
    division_by_zero = 1 / 0
    return {"detail": "This should not be returned."}
