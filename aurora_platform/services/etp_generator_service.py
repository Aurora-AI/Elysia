# src/aurora_platform/services/etp_generator_service.py

import uuid
from datetime import datetime

from aurora_platform.schemas.etp_schemas import ETPRequest, ETPResponse
from aurora_platform.services.knowledge_service import KnowledgeBaseService
from aurora_platform.services.llm_adapters import VertexAIAdapter


class ETPGeneratorService:
    """Serviço para geração de ETPs usando pipeline RAG"""

    def __init__(self, kb_service: KnowledgeBaseService):
        self.kb_service = kb_service
        self.llm_adapter = VertexAIAdapter()

    async def generate_etp(self, request: ETPRequest) -> ETPResponse:
        """Gera um ETP completo usando RAG e LLM"""

        # 1. Consultas RAG para recuperar contexto relevante
        queries = [
            f"estrutura padrão de ETP para {request.tipo_obra}",
            f"normas técnicas para obras de {request.tipo_obra}",
            f"especificações técnicas {request.tipo_obra}",
            "justificativa técnica obras públicas",
            "cronograma execução obras",
        ]

        contexto_rag = ""
        for query in queries:
            results = self.kb_service.retrieve(query=query, top_k=3)
            for doc in results:
                if doc.get("text"):
                    contexto_rag += f"\n{doc['text'][:500]}...\n"

        # 2. Construção do prompt estruturado
        prompt = f"""Você é um especialista em elaboração de Estudos Técnicos Preliminares (ETPs) para obras públicas.

CONTEXTO TÉCNICO RECUPERADO:
{contexto_rag}

DADOS DO PROJETO:
- Tipo de Obra: {request.tipo_obra}
- Local: {request.local}
- Objetivo: {request.objetivo}
- Valor Estimado: R$ {request.valor_estimado or "A definir"}
- Prazo Estimado: {request.prazo_estimado or "A definir"} dias

INSTRUÇÕES:
Gere um ETP completo em formato Markdown seguindo a estrutura padrão:

1. IDENTIFICAÇÃO DO PROJETO
2. JUSTIFICATIVA TÉCNICA
3. ESPECIFICAÇÕES TÉCNICAS
4. CRONOGRAMA PRELIMINAR
5. ESTIMATIVA DE CUSTOS
6. CONSIDERAÇÕES FINAIS

Use APENAS as informações fornecidas no contexto técnico. Seja preciso e técnico."""

        # 3. Geração via LLM
        conteudo_gerado = self.llm_adapter.generate(prompt)

        # 4. Preparação da resposta
        etp_id = str(uuid.uuid4())
        metadados = {
            "tipo_obra": request.tipo_obra,
            "local": request.local,
            "queries_utilizadas": len(queries),
            "contexto_chars": len(contexto_rag),
        }

        return ETPResponse(
            id=etp_id,
            conteudo_markdown=conteudo_gerado,
            status="gerado",
            data_geracao=datetime.utcnow(),
            metadados=metadados,
        )
