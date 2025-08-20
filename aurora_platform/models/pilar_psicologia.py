from sqlalchemy import Column, Integer, String, Text
from aurora_platform.core.db_legacy import Base


class PilarPsicologia(Base):
    __tablename__ = "pilar_psicologia"

    id = Column(Integer, primary_key=True, index=True)
    vies = Column(Text, nullable=False, comment="Vies cognitivo")
    descricao = Column(Text)
    impacto = Column(Text)
    fonte = Column(String(255))
    referencia = Column(String(255))
