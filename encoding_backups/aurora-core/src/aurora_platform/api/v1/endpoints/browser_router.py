from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from src.aurora_platform.schemas.browser_schemas import SummarizeURLRequest
from src.aurora_platform.services.browser_engine import BrowserEngine

router = APIRouter(prefix="/browser", tags=["Browser Engine"])


@router.post("/summarize-url", response_class=JSONResponse)
async def summarize_url(request: SummarizeURLRequest):
    try:
        engine = BrowserEngine()
        result = await engine.fetch_and_summarize(url=request.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao resumir URL: {str(e)}")
