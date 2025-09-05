## Plano de Refatoração — Preparação para LangGraph v0.6.5

Objetivo: mapear em detalhe cada ficheiro/função que precisa de mudança para suportar a migração para LangGraph v0.6.5, justificar a alteração e propor uma implementação de baixo risco com testes.

Checklist (requisitos da entrega)

- [x] Listar ficheiros apontados no `impact_map.md` e identificar funções/métodos relevantes.
- [x] Para cada função: justificar a mudança, indicar o tipo de alteração (API/assinatura/async), e propor testes a adicionar.
- [x] Indicar riscos conhecidos e passos de mitigação (dependências / lockfile).
- [x] Fornecer passos concretos para a Fase 2 (implementar, testar, lock/CI).

Resumo executivo
– A varredura inicial mostra que o código depende de adaptadores sincrónicos (`generate`) e de serviços de orquestração internos (orchestrator stub). A migração para LangGraph v0.6.5 exige centralizar o ponto de integração com o runtime de orquestração, adaptar assinaturas async e garantir mocks nos testes.

Artefactos gerados

- `analysis/refactor_plan.md` (este ficheiro) — plano detalhado

Per-file (detalhado)

1. `aurora_platform/modules/rag/orchestrator.py`

   - Funções/locais principais: `AuroraIngestionOrchestrator.__init__`, `AuroraIngestionOrchestrator.ingest_document` (async).
   - Assinaturas encontradas (excerto):

   ```py
   class AuroraIngestionOrchestrator:
     def __init__(self):
       pass

     async def ingest_document(self, document_data: dict) -> dict:
       return {"status": "success", "message": "Document ingested successfully"}
   ```

   - Situação atual: stub que devolve {"status":"success"}.
   - Mudanças propostas:
     - Implementar uma camada de "OrchestratorAdapter" que encapsula chamadas ao cliente LangGraph.
     - `ingest_document` deve delegar para `OrchestratorAdapter.run_ingest_workflow(document_data)` e tratar timeouts/exceptions.
     - Adicionar interface assíncrona e respeitar cancelamento/timeout (ex.: `asyncio.wait_for` com timeout configurável).
   - Justificação técnica: centralizar a integração com LangGraph facilita upgrades (apenas o adapter muda quando a client API mudar).
   - Testes a adicionar:
     - Unit test que injeta um Adapter mock (método `run_ingest_workflow` que lança/retorna) — validar comportamento em sucesso, timeout e erro.

2. `aurora_platform/api/v1/hub/rule_based_router.py`

   - Funções/locais principais: `RuleBasedRouter.__init__`, `RuleBasedRouter.route` (async).
   - Assinatura / excerto:

   ```py
   class RuleBasedRouter:
     def __init__(self, kb_service):
       ...

     async def route(self, request: HubRequest) -> HubResponse:
       task_lower = request.task.lower()
       for keyword, agent in self.rules.items():
         if keyword in task_lower:
           etp_request = ETPRequest(**request.payload)
           result = await agent.generate_etp(etp_request)
           return HubResponse(result=result, agent=agent.__class__.__name__)
   ```

   - Situação atual: roteia por substring e chama `agent.generate_etp(etp_request)` (assume async `generate_etp`).
   - Mudanças propostas:
     - Validar o contrato do `ETPGeneratorService`: garantir que `generate_etp` é `async` e aceita `ETPRequest`.
     - Introduzir um pequeno adaptador `AgentInvoker` que normaliza chamadas (suporta sync/async adapters).
   - Justificação técnica: LangGraph pode orquestrar agentes com diferentes assinaturas; um invoker unifica o uso.
   - Testes a adicionar:
     - Mock do `ETPGeneratorService` com async/sync variants; teste `route` devolve `HubResponse` consistente.

3. `aurora_platform/api/v1/hub/schemas.py`

   - Tipos: `HubRequest`, `HubResponse`.
   - Mudanças propostas:
     - Confirmar shape com as mensagens/inputs esperados pelo novo runtime LangGraph (se houver campos adicionais, adicionar versão `v2` dos schemas ou campos opcionais).
     - Documentar compatibilidade (convertors) entre `HubRequest.payload` e as mensagens de LangGraph.
   - Justificação técnica: evitar regressões quando o runtime passar a enviar/receber envelopes de mensagens diferentes.
   - Testes a adicionar: validação de serialização/deserialização entre schema e payloads de LangGraph stub.

4. `aurora_platform/services/adapter_factory.py`

   - Função: `AdapterFactory.create_adapter(provider_name: str) -> ILLMAdapter`.
   - Assinatura / excerto:

   ```py
   class AdapterFactory:
     @staticmethod
     def create_adapter(provider_name: str) -> ILLMAdapter:
       provider_name = provider_name.lower()
       if provider_name == "google":
         return VertexAIAdapter()
       elif provider_name == "azure":
         return AzureOpenAIAdapter()
       elif provider_name == "deepseek":
         return DeepSeekAdapter()
       else:
         raise ValueError(...)
   ```

   - Situação atual: devolve adaptadores com método síncrono `generate`.
   - Mudanças propostas:
     - Expor um contrato async: `async def generate(... )` em `ILLMAdapter` (ou adicionar `async_generate` opcional).
     - Implementar um wrapper que chama `generate` em thread-pool se o adaptador for síncrono (compat mode).
   - Justificação técnica: LangGraph workflows preferem coroutines; ter adaptadores async evita blocos na execução do grafo.
   - Testes a adicionar: compat test com adaptador sync adaptado para async via wrapper.

5. `aurora_platform/services/rag_service.py`

   - Função: `answer_query(query: str, model_provider: str) -> str`.
   - Observações encontradas: chama `AdapterFactory.create_adapter(...); adapter.generate(final_prompt)` e `kb_service.retrieve(query, top_k=2)` — `KnowledgeService` actual expõe `query()`.
   - Mudanças propostas:
     - Normalizar chamadas para async: `async def answer_query(...)` e tornar `adapter.generate` awaitable.
     - Corrigir/alinhar uso do KB service (usar `query` ou adicionar alias `retrieve` em `KnowledgeService`).
     - Encapsular a criação de `KnowledgeBaseService` (injeção) para facilitar mocking.
   - Justificação técnica: alinhamento de assinaturas e injeção facilita testes e integração com LangGraph (onde a geração de texto pode ser invocada dentro de um nó async).
   - Testes a adicionar: unit tests que mockam adapter e KB, e um contrato de integração leve.

6. `aurora_platform/api/v1/endpoints/ingestion_router.py`

   - Função: `ingest_document` (endpoint) — cria `AuroraIngestionOrchestrator` e await `ingest_document`.
   - Mudanças propostas:
     - Garantir que o endpoint propaga corretamente códigos HTTP para erros de orquestração (ex.: 504 para timeout).
     - Remover lógica blocking e mover timeouts para o orchestrator-adapter.
   - Testes a adicionar: integração com um orchestrator stub que simula workflows longos e falhas.

7. `backend/app/services/docparser/` (todos os ficheiros relevantes)

   - Funções: `process_document_pipeline` (`pipeline.py`), endpoints em `main.py`.
   - Mudanças propostas:
     - Não há dependência direta de LangGraph, mas fornecer contrato claro para a orquestração: input (filename, bytes) → IngestResponse.
     - Garantir que `process_document_pipeline` documenta exceções e expõe tempo de processamento/telemetria para que o orchestrator possa reagir.
   - Testes a adicionar: timeouts, exceções de parser e retornos consistentes.

8. `aurora_platform/services/llm_adapters.py`

   - Funções/classes: `ILLMAdapter` interface, `VertexAIAdapter`, `AzureOpenAIAdapter`, `DeepSeekAdapter`, `GeminiAdapter`.
   - Mudanças propostas:
     - Tornar `generate` uma coroutine (`async def generate(self, prompt: str) -> str`) na interface e atualizar implementações.
     - Para libs que expõem sync APIs, usar `asyncio.to_thread` ou `anyio` para não bloquear.
     - Garantir que adapters retornam a mesma estrutura (string) e documentar erro/timeouts.
   - Testes a adicionar: adaptadores sync -> async compatibility tests; mock external SDKs.

9. `aurora_platform/services/knowledge_service.py`
   - Funções: `ingest`, `query`, `verify_connection_health`.
   - Mudanças propostas:
     - Definir claramente `retrieve(query, top_k)` ou adicionar alias que o resto do código usa.
     - Manter a API compatível com chamadas síncronas/assíncronas; se necessário, acrescentar `async` wrappers.
   - Testes a adicionar: integração com VectorStore mock e circuit-breaker behavior.

Observações sobre dependências e risco

- `poetry.lock` atualmente restringe `langgraph` a `<0.4`; migrar para `0.6.5` implica atualizar `pyproject.toml` e regenerar o lockfile. Prepare um branch isolado e um MR para isto.
- Potenciais conflitos: `numpy` version pinning (qdrant-client vs docling/paddle) — manter docling/paddle como extras opcionais ou mover processamento pesado para containers separados.

Plano de implementação (Fase 2 — passo a passo)

1. Criar `aurora_platform/orchestration/adapter.py` com interface `OrchestratorAdapter` (sync + async shims). Implementar um `LangGraphAdapter` stub que encapsula o client.
2. Refatorar `AuroraIngestionOrchestrator` para usar `OrchestratorAdapter`.
3. Atualizar `ILLMAdapter` para async e adicionar wrappers para compatibilidade.
4. Corrigir `rag_service.answer_query` para ser `async` e usar injeção de `KnowledgeBaseService`.
5. Adicionar testes unitários e fixtures (mocks) para cada adaptador e para o orchestrator.
6. Atualizar `pyproject.toml` com `langgraph = "^0.6.5"` e executar `poetry lock` em ambiente controlado; resolver conflitos e documentar alterações.

QA e gates (verificação rápida)

- Lint (ruff) — aplicar automaticamente e corrigir violações.
- Testes unitários — adicionar cobertura para todos os novos adapters e orchestrator paths.
- Smoke test end-to-end: rodar pequena orquestração com `LangGraphAdapter` mock e validar respostas no endpoint `/ingest`.

Entregáveis desta tarefa

- Este ficheiro `analysis/refactor_plan.md` (contrato e lista por ficheiro).
- Branch sugerido para Fase 2: `feature/langgraph-upgrade-0.6.5/impl-orchestrator-adapter`.

Próximos passos que eu irei executar se autorizado

- Implementar o `OrchestratorAdapter` e os wrappers async nos adapters (criar arquivos e testes mínimos). Em seguida, executar lint e testes locais.

-- Fim do plano --
