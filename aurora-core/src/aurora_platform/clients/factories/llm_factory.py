from src.aurora_platform.clients.adapters.llm_phi3_adapter import LLMPhi3Adapter


class LLMFactory:
    """
    Fábrica para instanciar adaptadores de LLM.
    """

    @staticmethod
    def get_adapter(adapter_name: str, config=None):
        if adapter_name == "phi3":
            return LLMPhi3Adapter(config)
        # Futuramente: adicionar outros adaptadores (Azure, Vertex, etc)
        raise ValueError(f"Adapter '{adapter_name}' não suportado.")
