import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from .schemas import IngestRequest, IngestResponse
from .pipeline import process_document_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Aurora DocParser++ Service")


@app.post("/ingest/url", response_model=IngestResponse)
async def ingest_document_url(source: IngestRequest):
    """Ingestão via JSON contendo uma URL."""
    if not source.url:
        raise HTTPException(
            status_code=400, detail="Campo 'url' é obrigatório.")

    logger.info(f"Simulando download de {source.url}")
    content = b"conteudo-simulado-url"
    # Pydantic HttpUrl ensures .path exists; still guard for safety
    path = source.url.path if hasattr(source.url, 'path') else ''
    tail = path.rsplit('/', 1)[-1] if path else ''
    filename = tail or 'documento_url.pdf'

    try:
        result = await process_document_pipeline(filename, content)
        return result
    except Exception as e:
        logger.exception("Erro no processamento de documento")
        raise HTTPException(
            status_code=500, detail=f"Falha no processamento: {e}")


@app.post("/ingest/file", response_model=IngestResponse)
async def ingest_document_file(file: UploadFile = File(...)):
    """Ingestão via upload de arquivo (multipart/form-data)."""
    try:
        content = await file.read()
        filename = file.filename or "documento_subido"
        result = await process_document_pipeline(filename, content)
        return result
    except Exception as e:
        logger.exception("Erro no processamento de documento via arquivo")
        raise HTTPException(
            status_code=500, detail=f"Falha no processamento: {e}")
