# Registro de Erro

- **Data/Hora:** 2025-07-21 10:00
- **Descrição:** Erro de conexão com ChromaDB ao rodar testes unitários.
- **Stacktrace:** ValueError: Could not connect to a Chroma server. Are you sure it is running?
- **Solução Aplicada:** Iniciar o serviço com `docker compose up -d chromadb` antes dos testes.
- **Referências:** https://docs.chromadb.com/
