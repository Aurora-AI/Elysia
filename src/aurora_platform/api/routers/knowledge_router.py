# src/aurora_platform/api/routers/knowledge_router.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Request, status
import tempfile
import os
import fitz  # PyMuPDF
from typing import Dict, Any

from src.aurora_platform.schemas.knowledge_schemas import KnowledgeQuery, SearchResult
from src.aurora_platform.services.knowledge_service import KnowledgeBaseService

# Cria a instância do roteador para este módulo
router = APIRouter()


def get_kb_service(request: Request) -> KnowledgeBaseService:
    """Obtém a instância compartilhada do KnowledgeBaseService do estado da aplicação."""
    return request.app.state.kb_service


@router.post("/knowledge/ingest-from-file", status_code=status.HTTP_201_CREATED)
async def ingest_from_file(
    file: UploadFile = File(...),
    kb_service: KnowledgeBaseService = Depends(get_kb_service),
):
    """
    Faz upload de um arquivo PDF, extrai seu texto e ingere na base de conhecimento.
    """
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Apenas arquivos PDF com nome são suportados."
        )

    # Cria um diretório temporário seguro para o arquivo
    temp_dir = tempfile.mkdtemp()
    temp_path = os.path.join(temp_dir, file.filename)

    try:
        # Salva o arquivo temporariamente
        with open(temp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Extrai texto do PDF usando PyMuPDF
        doc = fitz.open(temp_path)
        text = ""
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Usa getattr para contornar problemas de type checking
            text += getattr(page, "get_text")()
        doc.close()

        if not text.strip():
            raise HTTPException(
                status_code=422,
                detail="Não foi possível extrair texto do PDF ou o arquivo está vazio.",
            )

        # Prepara os dados e chama o serviço de ingestão
        doc_id = f"file_{file.filename}"
        metadata: Dict[str, Any] = {"source": "local_upload", "filename": file.filename}
        kb_service.add_document(document_id=doc_id, text=text, metadata=metadata)

        return {"message": "Arquivo ingerido com sucesso.", "document_id": doc_id}
    except Exception as e:
        # Garante que qualquer exceção inesperada seja tratada
        raise HTTPException(
            status_code=500, detail=f"Ocorreu um erro ao processar o arquivo: {e}"
        )
    finally:
        # Garante que os arquivos temporários sejam sempre removidos
        if os.path.exists(temp_path):
            os.remove(temp_path)
        if os.path.exists(temp_dir):
            os.rmdir(temp_dir)


# --- Outros endpoints do roteador (se existirem) ---
@router.post("/knowledge/search", response_model=SearchResult)
async def search_in_kb(
    query: KnowledgeQuery, kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    """Realiza uma busca semântica na base de conhecimento."""
    results = kb_service.retrieve(query=query.query, top_k=query.n_results)
    document_texts = [doc.get("text", "") for doc in results if doc.get("text")]
    return SearchResult(results=document_texts)
