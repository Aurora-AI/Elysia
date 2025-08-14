from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List, Dict, Any


class IngestRequest(BaseModel):
    """
    Modelo de entrada para ingestão de documento.
    Aceita URL ou upload de arquivo.
    """
    url: Optional[HttpUrl] = Field(
        None, description="URL do documento a ser processado."
    )


class IngestResponse(BaseModel):
    """
    Modelo de resposta do pipeline de processamento.
    """
    texto_markdown: str
    tabelas: List[Dict[str, Any]]
    imagens: List[Dict[str, Any]]
    metadados: Dict[str, Any]
    proveniencia: Dict[str, Any]
    custo: Dict[str, float]
