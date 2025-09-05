# ğŸ•·ï¸� DeepDive Scraper Service - Fluxo AssÃ­ncrono

ServiÃ§o refatorado para implementar corretamente o fluxo assÃ­ncrono do Firecrawl.

## ğŸ“‹ Funcionalidades Implementadas

### 1. FunÃ§Ã£o `crawl_and_save()`

- **Fluxo AssÃ­ncrono Completo**: Implementa o padrÃ£o job-based do Firecrawl
- **Polling Inteligente**: Verifica status do job a cada 10 segundos
- **Tratamento de Estados**: Lida com 'pending', 'scraping', 'completed', 'failed'
- **Salvamento em Markdown**: Arquivos organizados com metadados

### 2. Estados do Job

- `pending` - Job na fila de processamento
- `scraping` - Crawling em andamento
- `completed` - Crawling concluÃ­do com sucesso
- `failed` - Erro durante o crawling

## ğŸš€ Como Usar

### Crawling AssÃ­ncrono

```python
# TODO: Reativar/substituir na integraÃ§Ã£o do Crawler.
# from src.aurora_platform.services.deep_dive_scraper_service import crawl_and_save

# Crawling completo de um site
result = crawl_and_save("https://example.com", "data/crawled")
print(result)  # "Crawling concluÃ­do. X arquivos salvos em data/crawled"
```

### Scraping Simples (PÃ¡gina Ãšnica)

```python
# TODO: Reativar/substituir na integraÃ§Ã£o do Crawler.
# from src.aurora_platform.services.deep_dive_scraper_service import scrape_url

# Scraping de uma pÃ¡gina especÃ­fica
data = await scrape_url("https://example.com")
```

## ğŸ”„ Fluxo de ExecuÃ§Ã£o

1. **InicializaÃ§Ã£o**: `app.crawl_url()` retorna `job_id`
2. **Polling Loop**:
   - Chama `app.check_crawl_status(job_id)`
   - Verifica status retornado
   - Aguarda 10 segundos se ainda processando
3. **FinalizaÃ§Ã£o**:
   - Status 'completed' â†’ Extrai dados e salva arquivos
   - Status 'failed' â†’ Levanta exceÃ§Ã£o com erro

## ğŸ“� Estrutura dos Arquivos Salvos

```
data/crawled/
â”œâ”€â”€ crawled_a1b2c3d4_0.md    # Primeira pÃ¡gina
â”œâ”€â”€ crawled_e5f6g7h8_1.md    # Segunda pÃ¡gina
â””â”€â”€ ...
```

### Formato dos Arquivos Markdown

```markdown
# TÃ­tulo da PÃ¡gina

**URL:** https://example.com/page

---

ConteÃºdo extraÃ­do da pÃ¡gina...
```

## âš™ï¸� ConfiguraÃ§Ã£o

Configure a chave da API no `config/.secrets.toml`:

```toml
[default]
FIRECRAWL_API_KEY = "sua-chave-aqui"
```

## ğŸ› ï¸� Tratamento de Erros

- **Job Failed**: ExceÃ§Ã£o com detalhes do erro
- **Timeout**: Loop infinito prevenido por estados vÃ¡lidos
- **API Key InvÃ¡lida**: Erro 401 capturado e reportado
- **Sem Dados**: ExceÃ§Ã£o se nenhum conteÃºdo for extraÃ­do

## ğŸ“Š Logs de Acompanhamento

Durante o crawling, o serviÃ§o exibe:

```
Iniciando crawling de: https://example.com
Job ID: abc123
Status do job: pending... aguardando...
Status do job: scraping... aguardando...
Crawling concluÃ­do!
Salvo: data/crawled/crawled_a1b2c3d4_0.md
Crawling concluÃ­do. 3 arquivos salvos.
```

## ğŸ”§ Melhorias de Robustez

### ValidaÃ§Ã£o de ConfiguraÃ§Ã£o

- âœ… **Validador Pydantic**: `@field_validator` para `FIRECRAWL_API_KEY`
- âœ… **Limpeza AutomÃ¡tica**: Remove espaÃ§os em branco com `strip()`
- âœ… **ValidaÃ§Ã£o de Nulidade**: Impede chaves vazias ou nulas

### Sistema de Logging

- âœ… **Logging Estruturado**: Substitui `print` por `logging`
- âœ… **Rastreabilidade**: Logs com timestamp e nÃ­vel
- âœ… **DepuraÃ§Ã£o**: Mostra primeiros caracteres da API key
- âœ… **Monitoramento**: Logs de status durante polling

### DiferenÃ§as da VersÃ£o Anterior

- âœ… **Antes**: `print` statements simples
- âœ… **Agora**: Sistema de logging profissional
- âœ… **Antes**: Sem validaÃ§Ã£o de API key
- âœ… **Agora**: ValidaÃ§Ã£o robusta com Pydantic
- âœ… **Antes**: Tentativa de extraÃ§Ã£o direta (falhava)
- âœ… **Agora**: Fluxo job-based correto com polling
