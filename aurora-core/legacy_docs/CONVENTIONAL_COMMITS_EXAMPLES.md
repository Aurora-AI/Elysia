# Exemplos de Commits Convencionais

Este documento apresenta exemplos de mensagens de commit seguindo o padrão [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/).

## Tipos Comuns

- **feat:** Uma nova funcionalidade
- **fix:** Correção de bug
- **docs:** Mudanças apenas na documentação
- **style:** Formatação, sem alteração de código (espaços em branco, ponto e vírgula, etc)
- **refactor:** Refatoração de código
- **perf:** Melhoria de performance
- **test:** Adição ou ajuste de testes
- **chore:** Atualização de tarefas de build, dependências, etc

## Exemplos

```
feat(api): adicionar endpoint de autenticação JWT
fix(db): corrigir erro de conexão com PostgreSQL
refactor(core): extrair lógica de validação para serviço separado
chore(deps): atualizar dependências do Poetry
style: padronizar indentação dos arquivos Python
```

## Recomendações

- Use o imperativo no início da mensagem ("adicionar", "corrigir", "atualizar").
- Inclua escopo entre parênteses quando relevante (ex: `feat(api): ...`).
- Seja sucinto e claro.
