import logging

from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel

router = APIRouter()


class YoutubeTranscriptExtractionRequest(BaseModel):
    project_name: str
    ordem_servico_id: str
    channel_url: str


@router.post("/extract-youtube-transcripts", status_code=status.HTTP_202_ACCEPTED)
async def extract_youtube_transcripts(
    request_body: YoutubeTranscriptExtractionRequest,
    background_tasks: BackgroundTasks,
):
    """
    Inicia a extração de transcrições de todos os vídeos de um canal do YouTube,
    em segundo plano, salvando artefatos por projeto e ordem de serviço.
    """
    try:
        # Serviço YoutubeTranscriptExtractionService removido do Aurora-Core (CLEANUP-FINAL)
        raise HTTPException(
            status_code=501,
            detail="Serviço de extração de transcrições não está mais disponível no Aurora-Core.",
        )
    except Exception as e:
        logging.error(f"Erro ao iniciar extração de transcrições: {e}")
        raise HTTPException(
            status_code=500, detail=f"Erro ao iniciar extração: {str(e)}"
        )
