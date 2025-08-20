from sqlalchemy import Column, Integer, String, Text
from aurora_platform.core.db_legacy import Base


class PilarVendas(Base):
    __tablename__ = "pilar_vendas"

    id = Column(Integer, primary_key=True, index=True)
    metodologia = Column(Text, nullable=False)
    descricao = Column(Text)
    aplicabilidade = Column(Text)
    fonte = Column(String(255))
