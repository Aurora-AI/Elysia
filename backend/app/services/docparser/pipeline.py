import hashlib
from .schemas import IngestResponse
from .parsers.docling_parser import parse_with_docling
from .parsers.fallback_parser import parse_with_fallback


async def process_document_pipeline(filename: str, content: bytes) -> IngestResponse:
    """
    Orquestra o processamento do documento: tenta Docling, fallback se necessário.
    """
    try:
        parsed_data = parse_with_docling(content)
    except Exception:
        parsed_data = parse_with_fallback(content)

    hash_conteudo = hashlib.sha256(content).hexdigest()

    return IngestResponse(
        texto_markdown=parsed_data.get("texto_markdown", ""),
        tabelas=parsed_data.get("tabelas", []),
        imagens=parsed_data.get("imagens", []),
        metadados={
            "fonte": filename,
            "mime_type": "application/pdf",
            "hash_conteudo": hash_conteudo
        },
        proveniencia={},
        custo={"usd_total": 0.0001}
    )
