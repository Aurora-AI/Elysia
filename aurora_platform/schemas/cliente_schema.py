from typing import Optional

from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: Optional[str] = None
    endereco: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    id: str
    class Config:
        from_attributes = True
