# üîê Sistema de Autentica√ß√£o JWT - Aurora Core

Sistema completo de autentica√ß√£o baseado em tokens JWT (Access e Refresh Tokens).

## üìã Componentes Implementados

### 1. Servi√ßo de Autentica√ß√£o (`auth_service.py`)

- `create_access_token()` - Gera tokens de acesso
- `create_refresh_token()` - Gera refresh tokens
- `verify_password()` - Verifica senhas
- `get_password_hash()` - Gera hash de senhas
- `verify_token()` - Valida tokens JWT

### 2. M√≥dulo de Seguran√ßa (`security.py`)

- `get_current_user()` - Depend√™ncia FastAPI para autentica√ß√£o
- Extrai e valida tokens do cabe√ßalho Authorization

### 3. Roteador de Autentica√ß√£o (`auth_router.py`)

- `POST /auth/token` - Endpoint de login
- Retorna access_token e refresh_token
- Suporte a OAuth2PasswordRequestForm

## üîë Credenciais de Teste

```
Usu√°rio: admin
Senha: secret

Usu√°rio: user
Senha: secret
```

## üöÄ Como Usar

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

## üõ°Ô∏è Endpoints Protegidos

- `POST /mentor/sales/prepare-meeting` - Requer autentica√ß√£o JWT

## ‚öôÔ∏è Configura√ß√µes

As configura√ß√µes JWT s√£o carregadas do sistema h√≠brido Dynaconf + Pydantic:

- `SECRET_KEY` - Chave secreta para assinar tokens
- `ALGORITHM` - Algoritmo de criptografia (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Expira√ß√£o do access token (30 min)
- `REFRESH_TOKEN_EXPIRE_DAYS` - Expira√ß√£o do refresh token (7 dias)

## üß™ Teste Automatizado

Execute o teste completo:

```bash
poetry run python test_auth_system.py
```

## üîí Seguran√ßa

- Senhas s√£o hasheadas com bcrypt
- Tokens JWT assinados com chave secreta
- Valida√ß√£o autom√°tica de expira√ß√£o
- Prote√ß√£o contra tokens inv√°lidos
