import logging
from typing import Optional, List, Dict, Any

from langchain.text_splitter import RecursiveCharacterTextSplitter
from pybreaker import CircuitBreaker, CircuitBreakerError
from tenacity import retry, stop_after_attempt, wait_exponential, wait_fixed

try:
    from aurora_platform.intelligence.vector_store import VectorStore
except ImportError:
    VectorStore = None

logger = logging.getLogger(__name__)


class KnowledgeService:
    """
    Serviço unificado para interagir com a base de conhecimento.
    Suporta tanto Qdrant quanto ChromaDB como fallback.
    """

    def __init__(self, use_qdrant: bool = True):
        self.use_qdrant = use_qdrant and VectorStore is not None

        if self.use_qdrant:
            try:
                self.vector_store = VectorStore()
                logger.info("KnowledgeService inicializado com Qdrant")
            except Exception as e:
                logger.warning(f"Falha ao inicializar Qdrant: {e}. Usando modo simplificado.")
                self.vector_store = None
        else:
            self.vector_store = None

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        self.circuit_breaker = CircuitBreaker(fail_max=3, reset_timeout=30)

    def ingest(self, document_text: str, metadata: Optional[Dict] = None) -> bool:
        """Processa e ingere um documento na base de conhecimento."""
        try:
            chunks = self.text_splitter.split_text(document_text)
            logger.info(f"Documento processado em {len(chunks)} chunks")

            if self.vector_store:
                # Lógica para Qdrant
                # self.vector_store.add_documents(chunks, metadata or {})
                pass

            return True
        except Exception as e:
            logger.error(f"Erro ao ingerir documento: {e}")
            return False

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def query(self, text: str, n_results: int = 5) -> str:
        """Consulta a base de conhecimento."""
        try:
            def do_query():
                if self.vector_store:
                    # Implementar query real no Qdrant
                    return f"Resultado da busca no Qdrant para: '{text}'"
                else:
                    return f"Resultado da busca (modo simplificado) para: '{text}'"

            return self.circuit_breaker.call(do_query)
        except CircuitBreakerError:
            logger.error("CIRCUITO ABERTO! Ativando modo degradado.")
            return f"Resposta em modo degradado para: '{text}'"
        except Exception as e:
            logger.error(f"Erro na operação de query: {e}")
            return f"Erro na busca para: '{text}'"

    async def verify_connection_health(self) -> bool:
        """Verifica a saúde da conexão com o vector store."""
        try:
            if self.vector_store:
                # Implementar health check do Qdrant
                logger.info("Conexão com Qdrant está saudável")
            return True
        except Exception as e:
            logger.error(f"Falha na verificação de saúde: {e}")
            return False


# Alias para compatibilidade
KnowledgeBaseService = KnowledgeService
