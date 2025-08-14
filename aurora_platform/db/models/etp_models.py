# src/aurora_platform/db/models/etp_models.py

import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class ETPModel(SQLModel, table=True):
    """Modelo de banco de dados para ETPs gerados"""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    tipo_obra: str = Field(index=True)
    local: str
    objetivo: str
    valor_estimado: Optional[float] = None
    prazo_estimado: Optional[int] = None
    conteudo_markdown: str
    status: str = Field(default="gerado", index=True)
    data_geracao: datetime = Field(default_factory=datetime.utcnow)
    data_atualizacao: datetime = Field(default_factory=datetime.utcnow)
    metadados: str = Field(default="{}")  # JSON string para metadados
    usuario_id: Optional[str] = Field(default=None, index=True)
