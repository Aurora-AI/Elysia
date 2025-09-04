from fastapi import APIRouter

router = APIRouter()


@router.get("/sentry-debug")
async def trigger_error():
    # Esta rota intencionalmente causa um erro para testar o Sentry
    raise RuntimeError("Intentional error for Sentry testing")
    return {"detail": "This should not be returned."}
