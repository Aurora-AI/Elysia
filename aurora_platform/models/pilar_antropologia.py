from sqlalchemy import Column, Integer, String, Text
from aurora_platform.core.db_legacy import Base


class PilarAntropologia(Base):
    __tablename__ = "pilar_antropologia"

    id = Column(Integer, primary_key=True, index=True)
    conceito = Column(Text, nullable=False,
                      comment="Conceito antropológico central")
    variavel = Column(String(255))
    contexto = Column(Text)
    fonte = Column(String(255))
    referencia = Column(String(255))
