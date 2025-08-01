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
