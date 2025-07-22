import pytest
from src.aurora_platform.services.browser_automation.local_llm_service import (
    LocalLLMService,
)


def test_local_llm_service_summarize():
    service = LocalLLMService()
    texto = """
    O Aurora-Core é uma plataforma de IA modular para automação de processos, análise de dados e integração multi-cloud.
    Seu objetivo é acelerar a transformação digital de empresas, oferecendo recursos avançados de NLP, RAG e orquestração inteligente.
    """
    resumo = service.summarize(texto, max_length=60, min_length=10)
    assert isinstance(resumo, str)
    assert len(resumo) > 0
    print(f"Resumo gerado: {resumo}")
