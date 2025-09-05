# ğŸš€ Aurora Frontend - Chat Interativo

Frontend React/Next.js para interaÃ§Ã£o com o Mentor de Vendas IA do Aurora-Core.

## ğŸ› ï¸� InstalaÃ§Ã£o

```bash
# Instalar dependÃªncias
pnpm install

# Ou usando npm
npm install
```

## âš™ï¸� ConfiguraÃ§Ã£o

1. Configure a URL da API no arquivo `.env`:

```env
PUBLIC_API_URL=http://localhost:8000
```

2. Certifique-se de que o Aurora-Core estÃ¡ rodando na porta 8000:

```bash
# No diretÃ³rio raiz do Aurora-Core
poetry run uvicorn src.aurora_platform.main:app --reload --host 0.0.0.0 --port 8000
```

## ğŸš€ ExecuÃ§Ã£o

```bash
# Modo desenvolvimento
pnpm dev

# Ou usando npm
npm run dev
```

Acesse: http://localhost:3000

## ğŸ“‹ Funcionalidades

### ChatMentor Component

- âœ… **Input de texto** para nome do cliente
- âœ… **BotÃ£o de envio** com estados de loading
- âœ… **IntegraÃ§Ã£o com API** via axios
- âœ… **Tratamento de erros** completo
- âœ… **Interface responsiva** com design moderno
- âœ… **Feedback visual** para diferentes estados

### Endpoints Integrados

- `POST /mentor/sales/prepare-meeting` - Obter insights de vendas

## ğŸ�¨ Design

- **Gradientes modernos** com cores Aurora
- **AnimaÃ§Ãµes suaves** e transiÃ§Ãµes
- **Design responsivo** para mobile e desktop
- **Feedback visual** para interaÃ§Ãµes
- **Tratamento de estados** (loading, error, success)

## ğŸ”§ Estrutura

```
frontend/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ components/
â”‚   â”‚   â””â”€â”€ ChatMentor.tsx     # Componente principal
â”‚   â””â”€â”€ pages/
â”‚       â””â”€â”€ index.tsx          # PÃ¡gina de teste
â”œâ”€â”€ .env                       # ConfiguraÃ§Ãµes
â”œâ”€â”€ package.json              # DependÃªncias
â”œâ”€â”€ next.config.js            # ConfiguraÃ§Ã£o Next.js
â””â”€â”€ tsconfig.json             # ConfiguraÃ§Ã£o TypeScript
```

## ğŸ§ª Teste

1. Inicie o Aurora-Core backend
2. Inicie o frontend: `pnpm dev`
3. Acesse http://localhost:3000
4. Digite um nome de cliente no chat
5. Clique em "Enviar" para testar a integraÃ§Ã£o

## ğŸ“¡ API Integration

O componente faz requisiÃ§Ãµes para:

- **URL**: `${API_URL}/mentor/sales/prepare-meeting`
- **MÃ©todo**: POST
- **Body**: `{ "client_name": "Nome do Cliente" }`
- **Headers**: `Content-Type: application/json`

## ğŸ›¡ï¸� Tratamento de Erros

- âœ… **401 Unauthorized** - Erro de autenticaÃ§Ã£o
- âœ… **500 Internal Server Error** - Erro do servidor
- âœ… **ECONNREFUSED** - Servidor nÃ£o disponÃ­vel
- âœ… **ECONNABORTED** - Timeout na requisiÃ§Ã£o
- âœ… **ValidaÃ§Ã£o de input** - Campo obrigatÃ³rio

## ğŸ�¯ PrÃ³ximos Passos

- [ ] Adicionar histÃ³rico de conversas
- [ ] Implementar autenticaÃ§Ã£o
- [ ] Adicionar mais endpoints do mentor
- [ ] Melhorar UX com typing indicators
- [ ] Adicionar temas personalizÃ¡veis
