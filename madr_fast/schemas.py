from datetime import datetime as dt

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    computed_field,
    field_validator,
)


def func_sanitiza(text):
    return ' '.join(text.lower().split())


# Message ---
class Message(BaseModel):
    message: str


# Usuario ---
class UsuarioSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str

    @field_validator('username')
    def username_nao_deve_conter_espacos(cls, v):
        if ' ' in v:
            raise ValueError('username should not contain spaces')
        return v


class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class UsuarioUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    senha: str | None = None

    @field_validator('username')
    def verifica_username(cls, v):
        if not v:  # username pode ser None `on update`
            return v
        if ' ' in v:  # username não deve conter espaços
            raise ValueError('username should not contain spaces')
        return v


# Livro ---
class LivroSchema(BaseModel):
    input_titulo: str = Field(alias='titulo')
    ano: int = Field(gt=0, lt=dt.today().year)
    # TODO: ver id do romancista
    # romancista_id: int

    @computed_field
    def titulo(self) -> str:
        return func_sanitiza(self.input_titulo)


class LivroResponse(BaseModel):
    titulo: str
    ano: int


# Romancista ---
class RomancistaSchema(BaseModel):
    input_nome: str = Field(alias='nome')

    @computed_field
    def nome(self) -> str:
        return func_sanitiza(self.input_nome)


class RomancistaResponse(BaseModel):
    # TODO: adicionar id
    # id: int
    nome: str


# Token ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
