<<<<<<< HEAD
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer

from aurora_platform.core.config import settings
from aurora_platform.intelligence.vector_store import VectorStore

class KnowledgeService:
    """
    Serviço para interagir com a base de conhecimento (ex: Qdrant).
    """
    def __init__(self):
        self.vector_store = VectorStore()
        # A linha abaixo pode ser comentada se o modelo não for necessário na inicialização
        # self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        print("KnowledgeService inicializado.")

    def ingest(self, document_text: str, metadata: dict):
        """Processa e ingere um documento na base de conhecimento."""
        chunks = self.text_splitter.split_text(document_text)
        # embeddings = self.model.encode(chunks).tolist()
        print(f"Documento processado em {len(chunks)} chunks e pronto para ingestão.")
        # Lógica para adicionar no vector_store
        # self.vector_store.add_documents(chunks, embeddings, metadata)

    def query(self, text: str) -> str:
        """Placeholder para consultar a base de conhecimento."""
        return f"Resultado da busca para: '{text}'"
=======
import logging

from pybreaker import CircuitBreaker, CircuitBreakerError
from tenacity import retry, stop_after_attempt, wait_exponential, wait_fixed

import chromadb
from chromadb.api import ClientAPI
from chromadb.config import Settings

logger = logging.getLogger(__name__)


class KnowledgeBaseService:
    def __init__(self, host: str = "chromadb", port: int = 8000):
        self.host = host
        self.port = port
        self.client: ClientAPI = self._connect_with_retry()

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(3))
    def _connect_with_retry(self) -> ClientAPI:
        try:
            logger.info(f"Tentando conectar ao ChromaDB em {self.host}:{self.port}...")
            client = chromadb.HttpClient(
                host=self.host,
                port=self.port,
                settings=Settings(anonymized_telemetry=False),
            )
            client.heartbeat()
            logger.info("Conexão com ChromaDB estabelecida com sucesso.")
            return client
        except Exception as e:
            logger.warning(
                f"Falha ao conectar ao ChromaDB na inicialização. Tentando novamente... Erro: {e}"
            )
            raise

    async def verify_connection_health(self):
        try:
            logger.info("Verificando saúde da conexão com ChromaDB em background...")
            self.client.heartbeat()
            logger.info("Conexão com ChromaDB está saudável.")
        except Exception:
            logger.error(
                "Conexão com ChromaDB falhou na verificação de saúde. Tentando reconectar..."
            )
            try:
                self.client = self._connect_with_retry()
                logger.info("Reconexão com ChromaDB bem-sucedida.")
            except Exception as recon_e:
                logger.critical(
                    f"Falha crítica ao tentar reconectar com ChromaDB: {recon_e}"
                )

    def get_or_create_collection(self, name: str):
        return self.client.get_or_create_collection(name=name)

    circuit_breaker = CircuitBreaker(fail_max=3, reset_timeout=30)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
    def query(self, collection_name: str, query_texts: list[str], n_results: int = 5):
        try:

            def do_query():
                collection = self.get_or_create_collection(name=collection_name)
                return collection.query(query_texts=query_texts, n_results=n_results)

            return self.circuit_breaker.call(do_query)
        except CircuitBreakerError:
            logger.error("CIRCUITO ABERTO! Ativando modo degradado.")
            # Aqui você pode implementar lógica de fallback, se necessário
            raise
        except Exception as e:
            logger.error(f"Erro na operação de query: {e}")
            raise
>>>>>>> origin/main
