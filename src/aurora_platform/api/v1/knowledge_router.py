# ... (resto do arquivo knowledge_router.py) ...
@router.post("/search", response_model=SearchResult)
async def search_in_kb(
    query: KnowledgeQuery,
    kb_service: KnowledgeBaseService = Depends(get_kb_service)
):
    """Realiza uma busca semântica na base de conhecimento."""
    try:
        results = kb_service.search(
            # --- CORREÇÃO AQUI ---
            query_text=query.query,
            n_results=query.n_results
        )
        return SearchResult(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))