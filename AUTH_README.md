# 🔐 Sistema de Autenticação JWT - Aurora Core

Sistema completo de autenticação baseado em tokens JWT (Access e Refresh Tokens).

## 📋 Componentes Implementados

### 1. Serviço de Autenticação (`auth_service.py`)
- `create_access_token()` - Gera tokens de acesso
- `create_refresh_token()` - Gera refresh tokens
- `verify_password()` - Verifica senhas
- `get_password_hash()` - Gera hash de senhas
- `verify_token()` - Valida tokens JWT

### 2. Módulo de Segurança (`security.py`)
- `get_current_user()` - Dependência FastAPI para autenticação
- Extrai e valida tokens do cabeçalho Authorization

### 3. Roteador de Autenticação (`auth_router.py`)
- `POST /auth/token` - Endpoint de login
- Retorna access_token e refresh_token
- Suporte a OAuth2PasswordRequestForm

## 🔑 Credenciais de Teste

```
Usuário: admin
Senha: secret

Usuário: user
Senha: secret
```

## 🚀 Como Usar

### 1. Fazer Login
```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=secret"
```

**Resposta:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 2. Acessar Endpoint Protegido
```bash
curl -X POST "http://localhost:8000/mentor/sales/prepare-meeting" \
     -H "Authorization: Bearer SEU_ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"client_name": "Empresa XYZ"}'
```

## 🛡️ Endpoints Protegidos

- `POST /mentor/sales/prepare-meeting` - Requer autenticação JWT

## ⚙️ Configurações

As configurações JWT são carregadas do sistema híbrido Dynaconf + Pydantic:

- `SECRET_KEY` - Chave secreta para assinar tokens
- `ALGORITHM` - Algoritmo de criptografia (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Expiração do access token (30 min)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Expiração do refresh token (7 dias)

## 🧪 Teste Automatizado

Execute o teste completo:
```bash
poetry run python test_auth_system.py
```

## 🔒 Segurança

- Senhas são hasheadas com bcrypt
- Tokens JWT assinados com chave secreta
- Validação automática de expiração
- Proteção contra tokens inválidos
