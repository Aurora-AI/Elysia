Archived: GITHUB_COPILOT_INSTRUCTIONS.md (archival copy)

Refer to /docs/COPILOT_AGENT_CONSTITUTION.md for the canonical constitution.

# Instruções Copilot — Auditoria 360º Aurora

## Auditoria 360º (Aurora)

Sempre que solicitado, execute a seguinte auditoria 360º no monorepo Aurora-Plataform:

1. **Diretórios Legados**: Verifique se diretórios antigos como `apps` não existem.
2. **Configuração Única**: Certifique-se de que arquivos como `pyproject.toml`, `poetry.lock`, `docker-compose.yml` existem apenas na raiz do projeto.
3. **Estrutura de Serviços**: Para cada serviço esperado (`aurora-core`, `aurora-crawler`, `deepseek-r1`, `gpt-oss`), verifique se:
   - O diretório existe.
   - Possui um `Dockerfile`.
4. **Repositórios Git Aninhados**: Não deve haver subdiretórios `.git` fora da raiz.
5. **Relatório**: Se houver erros, liste-os. Se não houver, reporte "100% CONFORME".

# Códice de Execução do Copilot - V1.0

## Missão

Sua missão é executar as tarefas de desenvolvimento de baixo nível, seguindo os procedimentos operacionais padrão (SOPs) abaixo para garantir consistência e qualidade.

## SOP 1: Inicialização do Ambiente de Desenvolvimento

1.  Verifique se o `Poetry` está instalado.
2.  Execute `poetry install` para sincronizar as dependências do `pyproject.toml`.
3.  Execute `poetry run pre-commit install` para ativar os _hooks_ de qualidade de código.

## SOP 2: Aplicação de Qualidade de Código

1.  Antes de cada _commit_, execute o seguinte comando para formatar e verificar o código:
    ```bash
    poetry run pre-commit run --all-files
    ```
2.  Corrija quaisquer erros reportados pelo `Ruff` antes de prosseguir.

## SOP 3: Execução de Testes

1.  Para executar a suíte de testes completa, utilize o comando:
    ```bash
    poetry run pytest
    ```
2.  Para executar testes de um ficheiro específico:
    ```bash
    poetry run pytest apps/meu_servico/tests/test_meu_modulo.py
    ```
3.  Nenhum código deve ser comitado se os testes correspondentes estiverem a falhar.

## SOP 4: Realização de Commits

1.  Adicione os ficheiros modificados: `git add .`
2.  Execute o comando de _commit_ utilizando **obrigatoriamente** o padrão de _Conventional Commits_:
    ```bash
    git commit -m "feat(api): adiciona endpoint para o crawler"
    ```

## SOP 5: Interação com a Pipeline de CI/CD

1.  Após o `git push`, monitore a execução da pipeline no GitHub Actions.
2.  Se a pipeline falhar, analise os logs para identificar a causa (ex: falha em testes, erro de _linting_).
3.  Corrija o problema localmente, valide com os SOPs 2 e 3, e envie um novo _commit_ com a correção.

Essas instruções substituem scripts e arquivos de auditoria legados. Não mantenha arquivos de auditoria no repositório.
