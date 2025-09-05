"""
Configurações e constantes do Aurora Horizon Scanner.

Este módulo define parâmetros estáticos utilizados pelo agente,
como canais de YouTube a serem monitorados e categorias de interesse.
Os valores podem ser ajustados nas fases de implementação conforme
necessidade.
"""


def get_youtube_channels() -> list[str]:
    """
    Retorna a lista de URLs de canais do YouTube a serem monitorados.
    Estes canais devem produzir conteúdo relevante sobre IA, agentes,
    frameworks e tecnologias correlatas.
    """
    return [
        "https://www.youtube.com/@ronnaldhawk",
        "https://www.youtube.com/@TinaHuang1",
        "https://www.youtube.com/@airevolutionx",
        "https://www.youtube.com/@AI.Uncovered",
    ]


def get_interest_categories() -> list[str]:
    """
    Retorna as categorias temáticas de interesse para o agente.
    Estas categorias devem orientar a coleta e a priorização das descobertas.
    """
    return [
        "frameworks_de_agentes_de_ia",
        "arquiteturas_RAG_e_pipelines_hibridos",
        "bases_de_dados_vetoriais_e_multimodais",
        "modelos_de_linguagem_open_source",
        "tecnicas_de_inferencia_eficiente",
        "seguranca_aplicada_a_IA",
        "plataformas_e_protocolos_de_interoperabilidade",
    ]
