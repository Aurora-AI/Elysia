"""
Geração automatizada de ETP (Estudo Técnico Preliminar) usando integração real com RAG e LLMs corporativos.
"""

from typing import Dict, Optional

from src.aurora_platform.services.etp_generator_service import ETPGeneratorService, ETPRequest
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService
import asyncio


def gerar_etp_real(tipo_obra: str, local: str, objetivo: str, valor_estimado: Optional[float] = None, prazo_estimado: Optional[int] = None) -> str:
    """
    Gera um ETP completo, buscando informações reais na base de conhecimento RAG e estruturando conforme o template oficial.
    Não alucina: se não houver contexto suficiente, o campo é marcado explicitamente.
    """
    kb_service = KnowledgeBaseService()
    service = ETPGeneratorService(kb_service)
    request = ETPRequest(
        tipo_obra=tipo_obra,
        local=local,
        objetivo=objetivo,
        valor_estimado=valor_estimado,
        prazo_estimado=prazo_estimado
    )
    etp_response = asyncio.run(service.generate_etp(request))
    return etp_response.conteudo_markdown


# Exemplo de uso real

from typing import Optional

def exemplo_execucao(
    tipo_obra: str = "Sistema PCA para logística Redelog",
    local: str = "Rio de Janeiro, RJ",
    objetivo: str = "O sistema PCA visa otimizar processos logísticos da Redelog, conforme diretrizes do Estado do RJ.",
    valor_estimado: Optional[float] = 500000.00,
    prazo_estimado: Optional[int] = 180
) -> None:
    documento = gerar_etp_real(tipo_obra, local, objetivo, valor_estimado, prazo_estimado)
    print(documento)

if __name__ == "__main__":
    exemplo_execucao()
