# Manual de Tecnologias Proprietárias Aurora — Vol. 1
ID: AUR-TEC-MAN-001 · Versão: 1.0 · Classificação: Interno

## Sumário
1. Doutrina da Engenharia de Contexto
2. AuroraRouter (orquestração/Assembly of Experts)
3. Memória Ativa (RAG 2.0: híbrido, rerank, compressão) — Vector Store: Qdrant
4. HRM (neuro‑simbólico / trustware)
5. Execução Segura (WASM/WAMR)
6. Delegação por Incompletude Semântica
7. Diretrizes de Implementação (APIs, flags, custos)
8. Operação & Observabilidade
9. Roadmap de Evolução (MVP1..MVP4)

> Todos os serviços devem expor capacidades (spec) para descoberta pelo Router.
> Todo conhecimento persistente passa pela **Memória Ativa** (não armazenar estado local).
