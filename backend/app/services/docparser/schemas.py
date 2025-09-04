
from pydantic import BaseModel, Field, HttpUrl


class Metadata(BaseModel):
    fonte: str
    mime_type: str
    bytes: int
    sha256: str
    # legacy/Portuguese key expected by some callers/tests
    hash_conteudo: str | None = None
    num_paginas: int | None = None


class StepRecord(BaseModel):
    name: str
    started_ms: int
    ended_ms: int
    ok: bool
    notes: str | None = None


class Diagnostics(BaseModel):
    parser_usado: str
    versao_parser: str
    fallback: bool
    steps: list[StepRecord]
    planned_chunks: int | None
    embedding_model: str | None


class CostBreakdown(BaseModel):
    cpu_ms_parser: int
    usd_estimado: float


class TableSchema(BaseModel):
    headers: list[str]
    rows: list[list[str]]


class ImageSchema(BaseModel):
    url: HttpUrl | None = None
    caption: str | None = None


class IngestRequest(BaseModel):
    """
    Modelo de entrada para ingestão de documento.
    Aceita URL ou upload de arquivo.
    """

    url: HttpUrl | None = Field(
        None, description="URL do documento a ser processado."
    )


class IngestResponse(BaseModel):
    """Modelo de resposta do pipeline de processamento."""

    texto_markdown: str
    tabelas: list[TableSchema]
    imagens: list[ImageSchema]
    metadados: Metadata
    proveniencia: Diagnostics
    custo: CostBreakdown
