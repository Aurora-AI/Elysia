import logging
from transformers.pipelines import pipeline

logger = logging.getLogger(__name__)


class LocalLLMService:
    """
    Serviço para sumarização de texto usando um modelo local
    via HuggingFace Transformers, garantindo privacidade.
    """

    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        self.model_name = model_name
        self._summarizer = None
        self._load_pipeline()

    def _load_pipeline(self):
        """Carrega o pipeline do modelo de sumarização sob demanda."""
        if self._summarizer is None:
            try:
                logger.info(
                    f"Carregando modelo de sumarização local: {self.model_name}"
                )
                self._summarizer = pipeline("summarization", model=self.model_name)
                logger.info("Modelo de sumarização carregado com sucesso.")
            except Exception as e:
                logger.exception(
                    f"Falha ao carregar o pipeline do modelo '{self.model_name}': {e}"
                )
                raise

    def summarize(self, text: str, max_length: int = 256, min_length: int = 64) -> str:
        """Gera um resumo do texto fornecido."""
        if not self._summarizer:
            raise RuntimeError(
                "O pipeline de sumarização não foi inicializado corretamente."
            )

        try:
            # Limita o texto de entrada para evitar sobrecarga no modelo pequeno
            input_text = text[:8000]
            result = self._summarizer(
                input_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False,
            )
            return result[0]["summary_text"]
        except Exception as e:
            logger.exception(f"Falha ao gerar o resumo: {e}")
            return "Erro ao gerar o resumo."
