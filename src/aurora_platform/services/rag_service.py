# src/aurora_platform/services/rag_service.py

from langchain_core.prompts import ChatPromptTemplate
from .knowledge_service import KnowledgeBaseService

# --- MUDANÇA CRÍTICA: Importa a interface e a fábrica ---
from .llm_adapters import ILLMAdapter
from .adapter_factory import AdapterFactory


def answer_query(query: str, model_provider: str) -> str:
    """
    Responde a uma pergunta usando a cadeia RAG com um adaptador de LLM dinâmico.
    """
    print(f"INFO: RAG Service iniciado para o provedor: {model_provider}")

    # 1. Obter o adaptador correto usando a fábrica
    try:
        adapter: ILLMAdapter = AdapterFactory.create_adapter(model_provider)
    except ValueError as e:
        return str(e)

    # 2. Recuperar o contexto
    kb_service = KnowledgeBaseService()
    retrieved_docs = kb_service.retrieve(query, top_k=2)

    if not retrieved_docs:
        return "Não encontrei informação relevante na minha base de conhecimento para responder a esta pergunta."

    context = "\n\n---\n\n".join([doc.get("text", "") for doc in retrieved_docs])

    # 3. Montar o prompt (lógica inalterada)
    template = """
    Você é um assistente especialista e conciso. Sua tarefa é responder à pergunta do usuário.
    Você DEVE usar APENAS as informações do CONTEXTO fornecido abaixo para formular sua resposta.
    NÃO invente informações nem use conhecimento externo.
    Sintetize a informação em uma resposta clara e direta.

    ---
    CONTEXTO:
    {context}
    ---
    PERGUNTA:
    {query}
    ---
    RESPOSTA SINTETIZADA E CONCISA:
    """
    # Usamos uma substituição de string simples para o prompt final
    final_prompt = template.format(context=context, query=query)

    # 4. Gerar a resposta usando o método padronizado do adaptador
    print("INFO: Invocando o adaptador do LLM para síntese...")
    response = adapter.generate(final_prompt)

    print("INFO: Resposta sintetizada recebida do adaptador.")
    return response
