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

Essas instruções substituem scripts e arquivos de auditoria legados. Não mantenha arquivos de auditoria no repositório.
