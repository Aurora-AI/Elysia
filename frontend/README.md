# 🚀 Aurora Frontend - Chat Interativo

Frontend React/Next.js para interação com o Mentor de Vendas IA do Aurora-Core.

## 🛠️ Instalação

```bash
# Instalar dependências
pnpm install

# Ou usando npm
npm install
```

## ⚙️ Configuração

1. Configure a URL da API no arquivo `.env`:
```env
PUBLIC_API_URL=http://localhost:8000
```

2. Certifique-se de que o Aurora-Core está rodando na porta 8000:
```bash
# No diretório raiz do Aurora-Core
poetry run uvicorn src.aurora_platform.main:app --reload --host 0.0.0.0 --port 8000
```

## 🚀 Execução

```bash
# Modo desenvolvimento
pnpm dev

# Ou usando npm
npm run dev
```

Acesse: http://localhost:3000

## 📋 Funcionalidades

### ChatMentor Component
- ✅ **Input de texto** para nome do cliente
- ✅ **Botão de envio** com estados de loading
- ✅ **Integração com API** via axios
- ✅ **Tratamento de erros** completo
- ✅ **Interface responsiva** com design moderno
- ✅ **Feedback visual** para diferentes estados

### Endpoints Integrados
- `POST /mentor/sales/prepare-meeting` - Obter insights de vendas

## 🎨 Design

- **Gradientes modernos** com cores Aurora
- **Animações suaves** e transições
- **Design responsivo** para mobile e desktop
- **Feedback visual** para interações
- **Tratamento de estados** (loading, error, success)

## 🔧 Estrutura

```
frontend/
├── src/
│   ├── components/
│   │   └── ChatMentor.tsx     # Componente principal
│   └── pages/
│       └── index.tsx          # Página de teste
├── .env                       # Configurações
├── package.json              # Dependências
├── next.config.js            # Configuração Next.js
└── tsconfig.json             # Configuração TypeScript
```

## 🧪 Teste

1. Inicie o Aurora-Core backend
2. Inicie o frontend: `pnpm dev`
3. Acesse http://localhost:3000
4. Digite um nome de cliente no chat
5. Clique em "Enviar" para testar a integração

## 📡 API Integration

O componente faz requisições para:
- **URL**: `${API_URL}/mentor/sales/prepare-meeting`
- **Método**: POST
- **Body**: `{ "client_name": "Nome do Cliente" }`
- **Headers**: `Content-Type: application/json`

## 🛡️ Tratamento de Erros

- ✅ **401 Unauthorized** - Erro de autenticação
- ✅ **500 Internal Server Error** - Erro do servidor
- ✅ **ECONNREFUSED** - Servidor não disponível
- ✅ **ECONNABORTED** - Timeout na requisição
- ✅ **Validação de input** - Campo obrigatório

## 🎯 Próximos Passos

- [ ] Adicionar histórico de conversas
- [ ] Implementar autenticação
- [ ] Adicionar mais endpoints do mentor
- [ ] Melhorar UX com typing indicators
- [ ] Adicionar temas personalizáveis