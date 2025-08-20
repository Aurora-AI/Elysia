from sqlalchemy import Column, Integer, String, Text
from aurora_platform.core.db_legacy import Base


class PilarEstatistica(Base):
    __tablename__ = "pilar_estatistica"

    id = Column(Integer, primary_key=True, index=True)
    metodo = Column(Text, nullable=False)
    modelo = Column(String(255))
    metricas = Column(Text)
    fonte = Column(String(255))
    referencia = Column(String(255))
