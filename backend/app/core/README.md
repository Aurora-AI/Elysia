# cortex_logger — Auditoria do Córtex

## Resumo

O módulo `backend.app.core.cortex_logger` fornece utilitários para registar
metadados de execução de Ordens de Serviço (OS) numa base SQLite localizada em
`db/cortex.db`.

## API principal

- `log_execution(...)` — grava um registo completo na tabela `execution_logs`.
  Pode levantar exceções em caso de falhas (por exemplo, esquema inexistente).

- `safe_log_execution(os_id, agente_executor='script', status='SUCESSO', ...)`
  — wrapper não falho recomendado como padrão de utilização. Esta função:
  - Cria timestamps UTC automáticos.
  - Tenta gravar um registo via `log_execution`.
  - Em caso de falha, regista a exceção em logs e retorna `None` (nunca
    propaga a exceção).

## Política de utilização

Por decisão constitucional do agente (veja `docs/COPILOT_AGENT_CONSTITUTION.md`),
qualquer execução humana ou automatizada que constitua a conclusão de uma
Ordem de Serviço deve terminar com um registo de execução no Córtex.

## Recomendações práticas

- Use `safe_log_execution` como a ação final em scripts e tarefas para garantir
  que a tentativa de registo não altera o resultado da execução nem o código
  de saída.

- Se precisar de garantias fortes (por exemplo, em pipelines onde o registo é
  mandatório), use `log_execution` diretamente e trate/propague exceções
  conforme a política do pipeline.

- Para desenvolvimento local, execute:

  python3 scripts/init_cortex_db.py

para criar a base `db/cortex.db` com a tabela necessária.

## Localização

- Módulo: `backend/app/core/cortex_logger.py`
- Testes: `backend/app/core/tests/test_safe_cortex_logger.py`

## Changelog

- 2025-09-04: Adicionado `safe_log_execution` e testes/documentação iniciais.
