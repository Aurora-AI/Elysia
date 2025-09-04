
from sqlmodel import Column, Field, SQLModel
from sqlmodel import String as SQLString


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


class User(UserBase, table=True):
    __tablename__ = "users"  # type: ignore

    id: int | None = Field(default=None, primary_key=True, index=True)
    nome: str | None = Field(default=None, sa_column=Column(SQLString(100)))
    email: str = Field(
        sa_column=Column(SQLString(100), unique=True, index=True, nullable=False)
    )
    hashed_password: str = Field(sa_column=Column(SQLString, nullable=False))
    is_active: bool = Field(default=True, nullable=False)
    is_superuser: bool = Field(default=False, nullable=False)
    full_name: str | None = Field(default=None, sa_column=Column(SQLString(200)))
    hashed_refresh_token: str | None = Field(
        default=None, sa_column=Column(SQLString)
    )
    two_factor_secret: str | None = Field(default=None, sa_column=Column(SQLString))
    two_factor_enabled: bool = Field(default=False, nullable=False)


class UserCreate(UserBase):
    password: str
    nome: str | None = None


class UserRead(UserBase):
    id: int
    nome: str | None = None


class UserUpdate(SQLModel):
    email: str | None = None
    full_name: str | None = None
    nome: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_superuser: bool | None = None


class Token(SQLModel):
    access_token: str
    token_type: str
    refresh_token: str | None = None


class TokenData(SQLModel):
    username: str | None = None
