# Caminho: src/aurora_platform/db/models/cliente_model.py
from typing import Optional, Dict, Any
from sqlmodel import Field, SQLModel
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column

# --- Modelo Base ---
# Contém os campos compartilhados por todos os outros schemas.
class ClienteBase(SQLModel):
    nome_principal: str = Field(index=True, description="O nome principal ou razão social do cliente.")
    cnpj: Optional[str] = Field(default=None, unique=True, index=True, description="CNPJ único do cliente, para enriquecimento de dados.")
    
    # Este é o campo que materializa nosso Princípio de Customização.
    # Ele armazena um dicionário flexível (JSON) no banco de dados.
    atributos_customizados: Optional[Dict[str, Any]] = Field(
        default_factory=dict, 
        sa_column=Column(JSONB),
        description="Um dicionário para armazenar campos customizados definidos pelo usuário."
    )

# --- Modelo da Tabela do Banco de Dados ---
# Representa a tabela 'cliente' no banco de dados.
class Cliente(ClienteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

# --- Schemas para a API ---
# Usados para validação de dados nas rotas da API.

class ClienteCreate(ClienteBase):
    """Schema para criar um novo cliente."""
    pass

class ClienteRead(ClienteBase):
    """Schema para retornar um cliente da API, incluindo o ID."""
    id: int

class ClienteUpdate(SQLModel):
    """Schema para atualizar um cliente. Todos os campos são opcionais."""
    nome_principal: Optional[str] = None
    cnpj: Optional[str] = None
    atributos_customizados: Optional[Dict[str, Any]] = None