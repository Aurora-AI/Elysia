"""
Módulo de coleta do Aurora Horizon Scanner.

Este módulo define funções responsáveis por extrair informações de diversas
fontes (papers, RFCs, changelogs, releases e vídeos de YouTube). As funções
de coleta são intencionadas a serem assíncronas e extensíveis, permitindo a
integração de novos tipos de fonte conforme o roadmap evolui.

Nesta fase inicial, apenas as assinaturas e docstrings são definidas.
"""

from typing import Any


def collect_from_papers() -> list[dict[str, Any]]:
    """
    Coleta metadados e resumos de papers de interesse.

    Returns:
        Uma lista de dicionários contendo título, resumo, autores e URL.

    Raises:
        NotImplementedError: Função ainda não implementada nesta fase.
    """
    raise NotImplementedError(
        "Função collect_from_papers ainda não implementada.")


def collect_from_changelogs() -> list[dict[str, Any]]:
    """
    Coleta informações de changelogs e releases de frameworks ou bibliotecas.

    Returns:
        Uma lista de entradas de changelog com descrição e link para a versão.

    Raises:
        NotImplementedError: Função ainda não implementada nesta fase.
    """
    raise NotImplementedError(
        "Função collect_from_changelogs ainda não implementada.")


def collect_from_rfc() -> list[dict[str, Any]]:
    """
    Coleta informações de RFCs relevantes para o domínio da IA e sistemas distribuídos.

    Returns:
        Uma lista de dicionários com metadados das RFCs coletadas.

    Raises:
        NotImplementedError: Função ainda não implementada nesta fase.
    """
    raise NotImplementedError(
        "Função collect_from_rfc ainda não implementada.")


def collect_from_youtube() -> list[dict[str, Any]]:
    """
    Coleta metadados de vídeos e, quando possível, transcrições de canais de YouTube.

    Returns:
        Uma lista de dicionários contendo título, descrição, data e link.

    Raises:
        NotImplementedError: Função ainda não implementada nesta fase.
    """
    raise NotImplementedError(
        "Função collect_from_youtube ainda não implementada.")
