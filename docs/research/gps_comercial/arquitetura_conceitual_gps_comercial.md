# Arquitetura Conceitual do GPS Comercial

## Modelo Preditivo Multifatorial
O score de saúde é composto por quatro vetores principais:
- **Dados Fundamentais do CRM:** Valor do negócio, estágio, data de fechamento prevista, probabilidade, datas de criação/modificação.
- **Engajamento:** Recência, frequência, reciprocidade, envolvimento de múltiplos stakeholders.
- **Risco:** Estagnação de estágio, silêncio de rádio, sinais contextuais (ex: menção de concorrente), mudança de decisor, score preditivo futuro.
- **Progressão:** Velocidade do pipeline, contagem de pushes, mudanças de valor, movimento de estágio.

### Métricas Específicas por Vetor
- **Engajamento:**
  - Recência: Dias desde o último toque significativo
  - Frequência: Número de interações recentes
  - Reciprocidade: Proporção de respostas do cliente
  - Multi-threading: Número de contatos distintos envolvidos
- **Risco:**
  - Estagnação de estágio
  - Falta de engajamento
  - Sinais contextuais (palavras-chave, mudança de decisor)
- **Progressão:**
  - Tempo entre estágios
  - Número de adiamentos (pushes)
  - Alterações de valor
  - Regressão de estágio

## Lógica de Cálculo do Score (MVP)
- Para cada negócio, buscar todos os campos de dados brutos especificados no dicionário de dados.
- Calcular sub-scores normalizados (0-100) para cada vetor.
- Score de cada vetor = média ponderada dos sub-componentes.
- Score Geral = média ponderada dos quatro vetores (exemplo: 40% Engajamento, 30% Risco, 20% Progressão, 10% CRM).
- Pesos e limiares configuráveis.
- MVP: modelo baseado em regras; evolução futura para Machine Learning.

## Dicionário de Dados de Integração
| Métrica                  | Salesforce                | HubSpot                  | Pipedrive                |
|-------------------------|---------------------------|--------------------------|--------------------------|
| Valor do Negócio        | Amount                    | amount                   | value                    |
| Estágio do Pipeline     | StageName                 | dealstage                | stage_id                 |
| Data de Fechamento      | CloseDate                 | closedate                | expected_close_date      |
| Probabilidade           | Probability               | hs_deal_stage_probability| probability (custom)     |
| Data Criação/Modificação| CreatedDate, LastModifiedDate | hs_lastmodifieddate | add_time, update_time    |
| Atividades/Engajamento  | Task, Event               | Engagements (CALL, EMAIL, MEETING) | /activities (deal_id)   |
