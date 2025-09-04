
from pydantic import BaseModel, EmailStr


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: str | None = None
    endereco: str | None = None


class ClienteCreate(ClienteBase):
    pass


class Cliente(ClienteBase):
    id: str

    class Config:
        from_attributes = True
