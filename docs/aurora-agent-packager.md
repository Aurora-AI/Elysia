# Aurora Agent - Packager

Este agente automatiza o processo de adição de dependências ao Aurora-Core, sob rígidas regras de governança.

## Fluxo de Trabalho

1. **Trigger:** Issue com label `new-dependency`.
2. **Extração:** Nome do pacote extraído do corpo da issue.
3. **Validação:** Verifica se o pacote está em `approved_packages.json`.
   - Se SIM: adiciona normalmente.
   - Se NÃO: adiciona label `security-review-required` e insere aviso no PR.
4. **Controle:** Nenhum PR é mesclado automaticamente; revisão humana obrigatória.
5. **Notificação:** Core team (@aurora-dev/core-team) é mencionada no PR.

## Atualização da Allowlist

- Atualize `approved_packages.json` para incluir novas dependências aprovadas.