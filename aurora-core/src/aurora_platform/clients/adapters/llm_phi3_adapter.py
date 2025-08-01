class LLMPhi3Adapter:
    """
    Adapter para integração com o modelo Phi-3.
    """

    def __init__(self, config):
        self.config = config

    def generate(self, prompt: str) -> str:
        # Aqui entraria a chamada real ao modelo Phi-3
        return f"[Phi-3] Resposta simulada para: {prompt}"
