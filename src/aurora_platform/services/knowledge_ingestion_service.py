# src/aurora_platform/services/knowledge_ingestion_service.py
import os
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def ingest_documents(source_directory: str):
    """Ingere documentos de texto em um banco de dados vetorial ChromaDB."""

    print("Carregando documentos...")
    documents = []
    for filename in os.listdir(source_directory):
        if filename.endswith(".txt"):
            filepath = os.path.join(source_directory, filename)
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())

    print("Dividindo em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print("Gerando embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("Armazenando vetores...")
    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory="chroma_db"
    )

    print("Ingestão concluída.")


if __name__ == "__main__":
    ingest_documents("./data/knowledge_base/")
