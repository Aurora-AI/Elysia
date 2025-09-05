# Impact map (LangGraph v0.6.5)

This document lists repository locations that implement orchestration, agent routing, and any likely LangGraph integration points. Each entry includes a short rationale and suggested inspection/changes.

1. aurora_platform/modules/rag/orchestrator.py

   - Rationale: Core orchestrator for ingestion and RAG flows. Likely to call into graph/orchestration APIs.
   - Inspect: how agents/tasks are registered and invoked; client instantiation; async/await usage.

2. aurora_platform/api/v1/hub/rule_based_router.py

   - Rationale: Hub router delegates tasks to concrete agent services (ETPGeneratorService). Confirm how agents are represented and invoked.
   - Inspect: agent invocation patterns and expected signatures for generate_etp / generate functions.

3. aurora_platform/api/v1/hub/schemas.py

   - Rationale: HubRequest/HubResponse define payload shapes used across orchestration; check compatibility with new LangGraph message shapes.

4. aurora_platform/services/adapter_factory.py

   - Rationale: Adapter factory constructs LLM adapters used by agents; LangGraph may assume different adapter interfaces or async patterns.

5. aurora_platform/services/rag_service.py

   - Rationale: High-level RAG flow which may be called by orchestrators; confirm how adapters are called (generate signature).

6. aurora_platform/api/v1/endpoints/ingestion_router.py

   - Rationale: Endpoint that creates AuroraIngestionOrchestrator and calls ingest_document; verify orchestration flow and any LangGraph runtime usage.

7. aurora_platform/api/v1/hub/rule_based_router.py

   - Rationale: Rule-based mapping from tasks to agents; ensure handlers remain compatible.

8. backend/app/services/docparser/

   - Rationale: New DocParser++ service — if integrated into AuroraRouter flows, confirm call contract and error/timeout handling.

9. tests and integration suites (aurora-core/tests and aurora-core/src/...)
   - Rationale: Update/add tests to cover orchestration flows and any adapters that interact with LangGraph.

Suggested immediate actions per-file:

- Search for direct imports of `langgraph` or `LangGraphClient` and wrap them with adapters to centralize changes.
- Add tests that mock langgraph client behaviour (simulate new API signatures).
- Pin pre-upgrade baseline tags so `evals` can compare before/after.

Next steps:

- For each file above, open and document the exact functions to refactor (I will iterate file-by-file if you want).
- Collect the official changelog items and map them to the functions/methods listed here.
