from __future__ import annotations

from typing import Optional, Dict, Any

from sqlalchemy import Integer, String, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column

from aurora_platform.core.db_legacy import Base


class PilarVendas(Base):
    __tablename__ = "pilar_vendas"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True)
    pilar_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)

    titulo: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    descricao: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fonte: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    versao: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    extra: Mapped[Optional[Dict[str, Any]]
                  ] = mapped_column(JSON, nullable=True)
