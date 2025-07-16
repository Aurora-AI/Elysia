# Aurora-Core: O Kernel do Sistema Operacional de IA (AIOS) Aurora

## 1. Visão do Projeto

O **Aurora-Core** não é apenas uma API de backend; é o **Kernel** do nosso **Sistema Operacional de Inteligência Artificial (AIOS)**. Este projeto representa a fundação sobre a qual todos os produtos e agentes inteligentes da Aurora são construídos. Nossa missão é criar um ecossistema de cognição distribuída, orquestrado por este Core.

A arquitetura é baseada nos princípios de:
- **Eficiência Radical:** Utilizando uma arquitetura híbrida e nossa tecnologia proprietária de "Delegação por Incompletude Semântica".
- **Fábrica de IA:** Usando IA para automatizar o design, a construção e os testes da própria plataforma.
- **Soberania Cognitiva:** Com o objetivo final de treinar e operar nossos próprios Modelos de Linguagem Fundamentais.

## 2. Arquitetura Técnica

- **Framework:** FastAPI
- **Linguagem:** Python 3.11+
- **Banco de Dados:** PostgreSQL com SQLModel e Alembic para migrações.
- **Gerenciamento de Dependências:** Poetry
- **Segurança:** Autenticação via Tokens JWT.
- **Configuração:** Sistema híbrido com Dynaconf e Pydantic para múltiplos ambientes.

## 3. Módulos Principais

- **Orquestrador Central (`AuroraRouter`):** O cérebro que roteia tarefas para o recurso mais eficiente.
- **Memória Ativa (RAG):** Nossa Unidade de Gerenciamento de Memória, usando ChromaDB para armazenar e recuperar conhecimento.
- **Camada de Percepção (`DeepDiveScraper`):** Nossos "sentidos" para coletar informações da web e de documentos.
- **Fábrica de IA (Ferramentas):** Inclui o `project_manager.py` e o `dashboard.py` para governança automatizada do projeto.

## 4. Como Começar

1.  **Instale as dependências:**
    ```bash
    poetry install
    ```
2.  **Configure o ambiente:**
    - Copie o arquivo `config/settings.example.toml` para `config/settings.toml`.
    - Copie o arquivo `config/.secrets.example.toml` para `config/.secrets.toml` e preencha com suas chaves de API e segredos.
3.  **Execute as migrações do banco de dados:**
    ```bash
    poetry run alembic upgrade head
    ```
4.  **Inicie o servidor de desenvolvimento:**
    ```bash
    poetry run uvicorn src.aurora_platform.main:app --reload
    ```
A API estará disponível em `http://127.0.0.1:8000/docs`.