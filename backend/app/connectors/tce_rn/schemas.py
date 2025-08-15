from __future__ import annotations
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, StrictStr, StrictFloat
from datetime import date, datetime


class RawApiExpense(BaseModel):
    orgao: Optional[str] = None
    unidade: Optional[str] = None
    fornecedor_nome: Optional[str] = None
    fornecedor_cnpj: Optional[str] = None
    empenho_numero: Optional[str] = None
    empenho_data: Optional[date] = None
    licitacao_modalidade: Optional[str] = None
    objeto: Optional[str] = None
    processo: Optional[str] = None
    classificacao_despesa: Optional[str] = None
    natureza_despesa: Optional[str] = None
    funcao: Optional[str] = None
    subfuncao: Optional[str] = None
    programa: Optional[str] = None
    acao: Optional[str] = None
    valor_empenhado: Optional[StrictFloat] = None
    valor_liquidado: Optional[StrictFloat] = None
    valor_pago: Optional[StrictFloat] = None
    competencia: Optional[str] = None
    municipio: Optional[str] = None
    uf: Optional[str] = None
    fonte_dados: Optional[str] = None
    id_registro: Optional[str] = None


class ExpenseRecord(BaseModel):
    source_system: Literal["TCE-RN"] = "TCE-RN"
    record_id: StrictStr = Field(...,
                                 description="ID único do registro na fonte")
    orgao: Optional[StrictStr] = None
    unidade: Optional[StrictStr] = None
    fornecedor_nome: Optional[StrictStr] = None
    fornecedor_cnpj: Optional[StrictStr] = None
    empenho_numero: Optional[StrictStr] = None
    empenho_data: Optional[date] = None
    licitacao_modalidade: Optional[StrictStr] = None
    objeto: Optional[StrictStr] = None
    processo: Optional[StrictStr] = None
    classificacao_despesa: Optional[StrictStr] = None
    natureza_despesa: Optional[StrictStr] = None
    funcao: Optional[StrictStr] = None
    subfuncao: Optional[StrictStr] = None
    programa: Optional[StrictStr] = None
    acao: Optional[StrictStr] = None
    valor_empenhado: Optional[StrictFloat] = None
    valor_liquidado: Optional[StrictFloat] = None
    valor_pago: Optional[StrictFloat] = None
    competencia: Optional[StrictStr] = None
    municipio: Optional[StrictStr] = None
    uf: Optional[StrictStr] = None
    fonte_dados: Optional[StrictStr] = None
    collected_at: datetime = Field(default_factory=datetime.utcnow)


class IngestEnvelope(BaseModel):
    connector: StrictStr = "tce_rn"
    schema: StrictStr = "expense_v1"
    items: List[ExpenseRecord]
