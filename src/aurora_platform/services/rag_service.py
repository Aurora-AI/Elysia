# src/aurora_platform/services/rag_service.py

from langchain_google_vertexai import VertexAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from aurora_platform.services.knowledge_service import KnowledgeBaseService

def answer_query(query: str) -> str:
    print("INFO: Iniciando a cadeia RAG para responder à consulta...")
    kb_service = KnowledgeBaseService()
    llm = VertexAI(model_name="gemini-1.5-flash-001")
    
    retrieved_docs = kb_service.retrieve(query, top_k=2)
    context = "\n\n".join([doc["text"] for doc in retrieved_docs if doc["text"]])

    template = """
    Você é a Aurora, uma assistente de IA especialista em análise de dados.
    Use os trechos de contexto a seguir para responder à pergunta no final.
    Se você não sabe a resposta, apenas diga que não sabe, não tente inventar uma resposta.
    Mantenha a resposta o mais concisa possível.

    Contexto:
    {context}

    Pergunta:
    {question}

    Resposta:
    """
    prompt = PromptTemplate.from_template(template)

    rag_chain = (
        {"context": lambda x: context, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    response = rag_chain.invoke(query)
    print("INFO: Resposta recebida do LLM.")
    return response