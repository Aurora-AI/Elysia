### CI & Housekeeping
- Adiciona workflow `PR Housekeeping` para auto-atribuir o autor em toda PR.
- Mantém CI existente; sem impacto funcional em runtime.

#### Test Plan
- Abrir/atualizar a PR: workflow deve rodar e definir o autor como assignee.

#### Rollout
- Merge squash; sem migrações, sem downtime.

#### Checklist
- [x] Workflow criado em `.github/workflows/pr-housekeeping.yml`
- [x] Execução em `pull_request` (opened/reopened/ready_for_review)
- [x] Permissão `pull-requests: write`
