from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()

class IngestRequest(BaseModel):
    source_dir: str

@router.post("/ingest", status_code=status.HTTP_202_ACCEPTED)
async def start_ingestion_pipeline(request: IngestRequest):
    # TODO: Chamar o pipeline de ingestão em background
    return {"message": "Processo de ingestão iniciado com sucesso.", "source_dir": request.source_dir}