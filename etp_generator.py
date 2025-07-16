"""
Geração automatizada de ETP (Estudo Técnico Preliminar) usando integração real com RAG e LLMs corporativos.
"""
from typing import Dict
from src.aurora_platform.services.etp_generator_service import ETPGeneratorService, ETPRequest

def gerar_etp_real(objeto_licitacao: str, valor_estimado: float, justificativa: str, modalidade_sugerida: str) -> str:
    """
    Gera um ETP completo, buscando informações reais na base de conhecimento RAG e estruturando conforme o template oficial.
    Não alucina: se não houver contexto suficiente, o campo é marcado explicitamente.
    """
    service = ETPGeneratorService()
    request = ETPRequest(
        objeto_licitacao=objeto_licitacao,
        valor_estimado=valor_estimado,
        justificativa=justificativa,
        modalidade_sugerida=modalidade_sugerida
    )
    return service.generate_etp(request)

# Exemplo de uso real
def exemplo_execucao():
    objeto_licitacao = "Sistema PCA para logística Redelog"
    valor_estimado = 500000.00
    justificativa = "O sistema PCA visa otimizar processos logísticos da Redelog, conforme diretrizes do Estado do RJ."
    modalidade_sugerida = "Concorrência Eletrônica"
    documento = gerar_etp_real(objeto_licitacao, valor_estimado, justificativa, modalidade_sugerida)
    print(documento)

if __name__ == "__main__":
    exemplo_execucao()
