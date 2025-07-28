# Plano Técnico: Gerador de ETPs

## Etapa 1: Configuração Base
**Objetivo:** Preparar ambiente e dependências
- Configurar endpoints específicos no Aurora-Core
- Adicionar dependências: `python-docx`, `PyMuPDF`
- Criar schemas Pydantic para ETP
- Configurar templates de ETP em Jinja2

## Etapa 2: Módulo de Ingestão de Documentos
**Objetivo:** Processar documentos de referência
- Estender `knowledge_router.py` para suportar DOCX
- Implementar extrator de entidades específicas (NER)
- Criar parser para links de legislação

## Etapa 3: Módulo RAG Especializado
**Objetivo:** Consulta inteligente para geração de ETP
- Criar `etp_service.py` com pipeline RAG customizado
- Implementar prompt engineering para ETP
- Configurar retrieval com filtros por tipo de obra
- Integrar com VertexAI (gemini-2.5-pro)

## Etapa 4: Endpoint da API
**Objetivo:** Interface para geração de ETP
- Criar `etp_router.py` com endpoints:
  - `POST /etp/generate` - Gerar ETP
  - `POST /etp/upload-reference` - Upload documentos
- Implementar validação de dados de entrada
- Configurar resposta em Markdown

## Etapa 5: Template Engine
**Objetivo:** Formatação padronizada do ETP
- Criar template base em Jinja2
- Implementar seções obrigatórias (Objetivo, Justificativa, Especificações)
- Configurar formatação automática
- Validar estrutura final
