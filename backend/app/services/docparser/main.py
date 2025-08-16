from fastapi import FastAPI, APIRouter, UploadFile, File, HTTPException, Request
from .schemas import IngestResponse
from .pipeline import process_document_pipeline
import hashlib
import logging

router = APIRouter(prefix="/v1/docparser", tags=["docparser"])
MAX_BYTES = 25 * 1024 * 1024  # 25 MB
ALLOWED_MIME = {"application/pdf", "text/html"}


def _sniff_mime(content: bytes, declared: str | None) -> str:
    # PDF signature
    if content[:5] == b"%PDF-":
        return "application/pdf"
    # crude HTML detection
    head = content[:256].lower()
    if b"<html" in head or b"<!doctype html" in head:
        return "text/html"
    # fallback to declared or octet-stream
    return declared or "application/octet-stream"


@router.post("/ingest", response_model=IngestResponse, status_code=200)
async def ingest_document(request: Request, file: UploadFile = File(...)):
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Arquivo vazio.")
    if len(content) > MAX_BYTES:
        raise HTTPException(status_code=413, detail="Arquivo excede o limite de 25MB.")

    sha256 = hashlib.sha256(content).hexdigest()
    sniffed = _sniff_mime(content, getattr(file, "content_type", None))
    if sniffed not in ALLOWED_MIME:
        raise HTTPException(status_code=415, detail=f"Tipo não suportado: {sniffed}")

    logger = logging.getLogger("docparser")
    logger.info(
        "ingest_request",
        extra={
            "event": "ingest_request",
            "filename": file.filename,
            "bytes": len(content),
            "sha256": sha256,
            "mime": sniffed,
        },
    )

    try:
        result = await process_document_pipeline(
            filename=file.filename or "upload.bin",
            content=content,
            sha256=sha256,
            sniffed_mime=sniffed,
        )
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("ingest_failed", extra={"sha256": sha256})
        raise HTTPException(status_code=500, detail="Falha no processamento.") from e


def create_app() -> FastAPI:
    app = FastAPI(
        title="Aurora DocParser++ Service",
        version="1.0.0",
        description="Serviço de ingestão e parsing de documentos (Fase 1).",
    )
    app.include_router(router)
    return app


# Uvicorn entrypoint: uvicorn backend.app.services.docparser.main:app --reload
app = create_app()
