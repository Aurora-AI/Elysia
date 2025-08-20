from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List


class Metadata(BaseModel):
    fonte: str
    mime_type: str
    bytes: int
    sha256: str
    # legacy/Portuguese key expected by some callers/tests
    hash_conteudo: Optional[str] = None
    num_paginas: Optional[int] = None


class StepRecord(BaseModel):
    name: str
    started_ms: int
    ended_ms: int
    ok: bool
    notes: Optional[str] = None


class Diagnostics(BaseModel):
    parser_usado: str
    versao_parser: str
    fallback: bool
    steps: List[StepRecord]
    planned_chunks: Optional[int]
    embedding_model: Optional[str]


class CostBreakdown(BaseModel):
    cpu_ms_parser: int
    usd_estimado: float


class TableSchema(BaseModel):
    headers: List[str]
    rows: List[List[str]]


class ImageSchema(BaseModel):
    url: Optional[HttpUrl] = None
    caption: Optional[str] = None


class IngestRequest(BaseModel):
    """
    Modelo de entrada para ingestão de documento.
    Aceita URL ou upload de arquivo.
    """

    url: Optional[HttpUrl] = Field(
        None, description="URL do documento a ser processado."
    )


class IngestResponse(BaseModel):
    """Modelo de resposta do pipeline de processamento."""

    texto_markdown: str
    tabelas: List[TableSchema]
    imagens: List[ImageSchema]
    metadados: Metadata
    proveniencia: Diagnostics
    custo: CostBreakdown
