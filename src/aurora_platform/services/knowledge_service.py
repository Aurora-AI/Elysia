import logging

from qdrant_client import QdrantClient

from src.aurora_platform.core.config import settings  # Nossa classe que lê o .env

logger = logging.getLogger(__name__)


class KnowledgeBaseService:
    def __init__(self):
        try:
            logger.info(f"Conectando ao Qdrant Cloud em: {settings.QDRANT_URL}")
            self.client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY,
                timeout=60,  # Aumenta o timeout para conexões de rede
            )
            logger.info("Conexão com Qdrant Cloud estabelecida com sucesso.")
        except Exception as e:
            logger.critical(f"Falha crítica ao conectar com Qdrant Cloud: {e}")
            raise

    # ... (resto da classe: query, add_documents, etc.)
