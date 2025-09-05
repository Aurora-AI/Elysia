# LangGraph Refactoring Plan (upgrade to v0.6.5)

This document maps files from `analysis/impact_map.md` to concrete refactor tasks required to upgrade to LangGraph v0.6.5.

---

## Summary of approach

For each file listed, I inspected the source to find where orchestration, adapter invocation, and agent routing occur. The plan below lists, per-file:

- Function/Class impacted
- Lines (approximate) to review/modify
- Short technical justification for the change
- Effort estimate (Low / Medium / High)

---

## 1) `aurora_platform/modules/rag/orchestrator.py`

- Function/Class to modify:

  - `AuroraIngestionOrchestrator.__init__` (class initializer)
  - `AuroraIngestionOrchestrator.ingest_document` (async method)

- Lines impacted: whole file (file is small). The method `ingest_document` is defined starting near the top of the file and returns a simulated dict.

- Justification:

  - The orchestrator is likely to integrate with LangGraph orchestration APIs. With v0.6.5 LangGraph may change how graphs are created, how nodes are invoked, and how async execution is awaited. Replace simulated behavior with a concrete orchestration client/factory.
  - Update to use a centralized `LangGraphAdapter` (see `services/adapter_factory`) so the orchestrator does not import LangGraph types directly. This centralizes changes and allows swapping implementations.

- Suggested changes:

  - Introduce `LangGraphAdapter` abstraction (if not present) and obtain it through `AdapterFactory` or a new `orchestrator_adapter_factory`.
  - Implement concrete orchestration calls using the adapter; handle new return schema (v0.6.5) and map to internal ingestion result.
  - Ensure async/await semantics align with LangGraph's new async execution model (some LangGraph calls may be sync or return an awaitable).

- Effort estimate: Medium

---

## 2) `aurora_platform/api/v1/hub/rule_based_router.py`

- Function/Class to modify:

  - `RuleBasedRouter.__init__`
  - `RuleBasedRouter.route`

- Lines impacted: The route method where `ETPGeneratorService.generate_etp` is awaited and `ETPRequest` is created.

- Justification:

  - Agent invocation patterns used by the router must match the agent interfaces expected by LangGraph v0.6.5. If `generate_etp` is now expected to be invoked through a graph node or receives different payload types, update adapter/agent wrappers.
  - Replace direct service instantiation with factory-injected adapters that present a stable `.generate_etp(...)` async interface.

- Suggested changes:

  - Use dependency injection to supply agent adapters (via `AdapterFactory`) rather than creating concrete service instances in `__init__`.
  - Ensure `route` validates payloads against new HubRequest->ETPRequest conversions and handles any new response wrapper from LangGraph.

- Effort estimate: Low

---

## 3) `aurora_platform/api/v1/hub/schemas.py`

- Function/Class to modify:

  - `HubRequest` and `HubResponse` Pydantic models

- Lines impacted: model definitions

- Justification:

  - LangGraph v0.6.5 might change message shapes or add metadata to responses (trace IDs, run state). Update HubResponse to include optional metadata fields (e.g., `run_id`, `status`, `node_logs`) and adapt callers.

- Suggested changes:

  - Add optional `meta: dict = {}` to `HubResponse` to carry any LangGraph runtime metadata without breaking schema.

- Effort estimate: Low

---

## 4) `aurora_platform/services/adapter_factory.py`

- Function/Class to modify:

  - `AdapterFactory.create_adapter`

- Lines impacted: entire factory logic that returns adapter instances.

- Justification:

  - Adapters that back agents (LLM or orchestration) may need to implement a new interface required by LangGraph v0.6.5 (e.g., different async signatures, lifecycle methods). The factory should be extended to produce `LangGraphAdapter` wrappers where appropriate.

- Suggested changes:

  - Introduce a `LangGraphAdapter` type and add mapping logic to instantiate a LangGraph-specific adapter when required (or provide a decorator that wraps existing adapters to the expected interface).
  - Centralize feature-detection for LangGraph version and provide shims for older/newer APIs.

- Effort estimate: Medium

---

## 5) `aurora_platform/services/rag_service.py`

- Function/Class to modify:

  - `answer_query` (function)

- Lines impacted: adapter acquisition and `adapter.generate` invocation.

- Justification:

  - The adapter generate method may now return richer objects or require different arguments. Adapt `answer_query` to call `adapter.generate(...)` with the updated signature or to unwrap the new response object.

- Suggested changes:

  - Wrap calls to `adapter.generate` in a compatibility shim that accepts both old (string) and new (object) return types and extracts the text.
  - Add error handling for LangGraph runtime errors and map them to user-friendly strings.

- Effort estimate: Low

---

## 6) `aurora_platform/api/v1/endpoints/ingestion_router.py`

- Function/Class to modify:

  - `ingest_document` endpoint

- Lines impacted: the creation and use of `AuroraIngestionOrchestrator` and the `await orchestrator.ingest_document(document_data)` call.

- Justification:

  - If orchestrator internals change to use LangGraph v0.6.5, ensure the endpoint handles any new exceptions or response metadata and sets an appropriate HTTP response (202 vs 200, returned run_id, etc.).

- Suggested changes:

  - Catch specific orchestration exceptions and return structured error responses.
  - Include optional `run_id` or `job_id` in the accepted response body when orchestrator returns it.

- Effort estimate: Low

---

## 7) `aurora_platform/api/v1/hub/rule_based_router.py` (duplicate entry)

- See entry #2. Ensure that any changes are idempotent and tests cover both hub and endpoint usage.

---

## 8) `backend/app/services/docparser/` (pipeline, parsers)

- Function/Class to modify:

  - `process_document_pipeline` (async function in `pipeline.py`)
  - `parse_with_docling` and `parse_with_fallback` parser functions

- Lines impacted: parsing calls and error handling region.

- Justification:

  - DocParser++ may be integrated into larger LangGraph flows; ensure parsers are pure functions (sync) or clearly annotated as `async` if they call async I/O. Keep their contract stable.

- Suggested changes:

  - Add explicit exception types and timeouts when calling external parser libraries.
  - Consider exposing a small adapter that conforms to LangGraph's expected node interface if parser is to be a node in a graph.

- Effort estimate: Low

---

## 9) Tests and integration suites

- Action:

  - Update or add unit/integration tests that mock LangGraph client behavior and validate that adapters and orchestrators handle both the previous and new LangGraph response shapes.

- Suggested changes:

  - Add `tests/mocks/langgraph_mock.py` providing compatibility responses and error scenarios.
  - Add tests for `AuroraIngestionOrchestrator` and `RuleBasedRouter` that patch adapters to use the mock and assert behavior.

- Effort estimate: Medium

---

## Overall priorities and next steps

1. Implement a `LangGraphAdapter` shim in `aurora_platform/services/adapter_factory.py` to centralize compatibility changes. (Medium)
2. Update `AuroraIngestionOrchestrator.ingest_document` to use adapter instead of direct LangGraph imports. (Medium)
3. Add tests/mocks for LangGraph responses and run the full test suite. (Medium)
4. Update schemas to accept optional LangGraph metadata fields. (Low)

---

## Notes & Assumptions

- Assumed that LangGraph v0.6.5 changes include altered invocation signatures, return types that carry metadata (run_id/status), and possibly changed async behaviors. Exact migration steps depend on the LangGraph changelog; once supplied, map concrete API swaps.
- Line numbers are approximated because some files are compact; I recommend searching for direct `langgraph` imports and `adapter.generate` usages to find exact edit sites.

---

Prepared by: GitHub Copilot (Agent Executor)
Date: 2025-08-15
