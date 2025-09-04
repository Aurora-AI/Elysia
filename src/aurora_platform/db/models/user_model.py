from typing import Optional

from sqlmodel import Column, Field, SQLModel
from sqlmodel import String as SQLString


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: Optional[str] = None


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    nome: Optional[str] = Field(default=None, sa_column=Column(SQLString(100)))
    email: str = Field(
        sa_column=Column(SQLString(100), unique=True, index=True, nullable=False)
    )
    hashed_password: str = Field(sa_column=Column(SQLString, nullable=False))
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    full_name: Optional[str] = Field(default=None, sa_column=Column(SQLString(200)))
    hashed_refresh_token: Optional[str] = Field(
        default=None, sa_column=Column(SQLString)
    )
    two_factor_secret: Optional[str] = Field(default=None, sa_column=Column(SQLString))
    two_factor_enabled: bool = Field(default=False, nullable=False)


class UserCreate(UserBase):
    password: str
    nome: Optional[str] = None


class UserRead(UserBase):
    id: int
    nome: Optional[str] = None


class UserUpdate(SQLModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    nome: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class Token(SQLModel):
    access_token: str
    token_type: str
    refresh_token: Optional[str] = None


class TokenData(SQLModel):
    username: Optional[str] = None
