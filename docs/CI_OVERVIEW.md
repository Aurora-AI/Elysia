# Aurora-Core CI/CD Overview

## Pipeline de Integração Contínua (CI)

O pipeline de CI do Aurora-Core foi refundado para garantir:

- Qualidade de código automatizada (Ruff para lint e formatação)
- Testes automatizados (pytest)
- Instalação e validação do ambiente via Poetry
- Modularidade para fácil extensão (frontend, build Docker, deploy, segurança)

### Branches Monitoradas

- main
- feature/\*
- bugfix/\*
- Pull Requests para qualquer uma dessas branches

### Etapas do Pipeline

1. **Checkout do repositório**
2. **Configuração do Python 3.11**
3. **Instalação do Poetry**
4. **Instalação das dependências**
5. **Verificação de formatação com Ruff**
6. **Lint com Ruff**
7. **Execução dos testes com Pytest**

### Governança

- Toda automação é versionada e auditável
- Nenhum resíduo de automação ou configuração de terceiros é versionado
- O pipeline é facilmente extensível para futuras integrações

### Exemplo de Conventional Commit para automação

```
chore(ci): refundação do pipeline CI/CD com Ruff e validação automatizada
```
