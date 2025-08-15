Cortex DB

Este diretório contém a base de dados SQLite usada como memória operacional (córtex).

- `cortex.db`: banco SQLite com a tabela `execution_logs`.

Como inicializar (local):

```bash
python3 scripts/init_cortex_db.py
```

Exemplo de uso do logger em Python:

```python
from backend.app.core.cortex_logger import log_execution
log_execution(os_id='AUR-XXX', timestamp_inicio='2025-08-15T12:00:00Z', timestamp_fim='2025-08-15T12:05:00Z', agente_executor='GitHub Copilot', status='SUCESSO')
```
