# src/aurora_platform/services/rag_service.py
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.aurora_platform.core.config import settings

async def answer_query(query: str) -> str:
    """Responde a uma pergunta usando RAG com ChromaDB e Gemini."""
    try:
        # Inicializar embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        
        # Carregar vector store
        vector_store = Chroma(
            persist_directory="chroma_db",
            embedding_function=embeddings
        )
        
        # Criar retriever
        retriever = vector_store.as_retriever(search_kwargs={"k": 2})
        
        # Recuperar documentos relevantes
        docs = retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in docs)
        
        # Usar Google Generative AI diretamente (mais confiável)
        from src.aurora_platform.intelligence.llm_interface import LLMInterface
        llm_interface = LLMInterface()
        
        prompt_text = f"""Você é um assistente especialista. Responda à pergunta do usuário baseando-se estritamente no seguinte contexto:

--- CONTEXTO:
{context}

--- PERGUNTA:
{query}
"""
        
        return llm_interface.generate_text(prompt_text)

        
    except Exception as e:
        return f"Erro ao processar consulta: {str(e)}"