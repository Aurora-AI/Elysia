# src/aurora_platform/schemas/etp_schemas.py

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ETPRequest(BaseModel):
    """Schema para requisição de geração de ETP"""

    tipo_obra: str = Field(
        ..., description="Tipo da obra (ex: Construção, Reforma, Pavimentação)"
    )
    local: str = Field(..., description="Local da obra")
    objetivo: str = Field(..., description="Objetivo do projeto")
    valor_estimado: Optional[float] = Field(None, description="Valor estimado da obra")
    prazo_estimado: Optional[int] = Field(None, description="Prazo estimado em dias")
    documentos_referencia: Optional[List[str]] = Field(
        default=[], description="IDs dos documentos de referência"
    )


class ETPResponse(BaseModel):
    """Schema para resposta da geração de ETP"""

    id: str = Field(..., description="ID único do ETP gerado")
    conteudo_markdown: str = Field(
        ..., description="Conteúdo do ETP em formato Markdown"
    )
    status: str = Field(..., description="Status da geração")
    data_geracao: datetime = Field(..., description="Data e hora da geração")
    metadados: dict = Field(default={}, description="Metadados adicionais")


class ETPStatus(BaseModel):
    """Schema para consulta de status de ETP"""

    id: str
    status: str
    progresso: int = Field(ge=0, le=100, description="Progresso em percentual")
