# LangGraph v0.6.5 changelog summary

Referências:

- Official release: https://github.com/langchain-ai/langgraph/releases/tag/v0.6.5

Resumo (alto nível):

- Correções de estabilidade em orquestração multi-ator.
- Melhorias de observabilidade e tracing integradas.
- Ajustes em APIs de cliente e mudanças em nomes de métodos (verificar breaking changes completos no release notes).

Notas importantes para a Aurora:

- A Aurora usa LangGraph para orquestração do "AuroraRouter" e pipelines de agentes; qualquer mudança de assinatura no client ou no runtime pode impactar a criação/registro de agentes e os fluxos de delegação.
- Antes do upgrade, executar full-scan de pontos de integração e testes de regressão em fluxos de orquestração (RAG/orchestrator/hub).
