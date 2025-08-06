# retrieve_knowledge.py

from src.aurora_platform.services.knowledge_service import KnowledgeBaseService

OUTPUT_FILE = "retrieved_knowledge.md"


def extract_all_knowledge():
    """
    Conecta-se à base de conhecimento e extrai todos os documentos armazenados.
    """
    print("INFO: Inicializando o serviço de base de conhecimento...")
    kb_service = KnowledgeBaseService()

    # Busca todos os documentos usando o método retrieve
    all_docs = kb_service.retrieve(query="", top_k=1000)  # Busca ampla

    print("INFO: Extraindo todos os documentos da coleção...")

    if not all_docs:
        print("AVISO: Nenhum documento encontrado na base de conhecimento.")
        return

    documents = [doc.get("text", "") for doc in all_docs]
    metadatas = [doc.get("metadata", {}) for doc in all_docs]

    print(
        f"INFO: {len(documents)} documentos extraídos. Salvando em '{OUTPUT_FILE}'..."
    )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, doc_text in enumerate(documents):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            source_url = metadata.get("sourceURL", "Fonte desconhecida")

            f.write(f"--- Documento {i+1} ---\n")
            f.write(f"Fonte: {source_url}\n")
            f.write("-------------------------------------\n\n")
            f.write(doc_text)
            f.write("\n\n\n")

    print(f"[OK] SUCESSO: Conhecimento extraído e salvo em '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    extract_all_knowledge()
