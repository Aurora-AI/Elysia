# Ontologia Inicial — Aurora KG (v1)

## Objetivo
Base conceitual mínima para os **Quatro Pilares**. Esta ontologia será expandida na próxima fase (MVPs Jurídico e Vendas).

## Nós
- **Pilar**
  - `id: string` (único) — ex.: PILAR-ANT, PILAR-PSI, PILAR-VEN, PILAR-EST
  - `name: string` — "Antropologia", "Psicologia", "Vendas", "Estatistica"
  - `titulo: string?`
  - `created_at: datetime`, `updated_at: datetime?`

> Nós específicos por domínio (futuro):
> - Jurídico: `PrincipioJuridico`, `Norma`, `Fato`, `Argumento`, `RiscoJuridico`
> - Vendas: “Play”, “Objeção”, “Métrica”, “Comprador”, etc.

## Relações (iniciais)
- `(Antropologia)-[:INFORMA]->(Vendas)`
- `(Psicologia)-[:INFLUENCIA]->(Vendas)`
- `(Estatistica)-[:MENSURA]->(Vendas)`

> Justificativa: Vendas é o palco de aplicação; Antropologia dá contexto, Psicologia modela atores, Estatística quantifica/valida.

## Regras de modelagem (guidelines)
- `MERGE` por `id` para idempotência.
- Evitar duplicar labels; manter propriedades canônicas.
- Sempre versionar mudanças estruturais no repositório (migrations Cypher).
