from datetime import datetime as dt

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    computed_field,
)


def func_sanitiza(text):
    return ' '.join(text.lower().split())


# Message ---
class Message(BaseModel):
    message: str


# Usuario ---
class UsuarioSchema(BaseModel):
    input_username: str = Field(alias='username')
    email: EmailStr
    senha: str

    # TODO: adicionar um validacao para caracteres especiais
    # @field_validator('username')
    # def username_nao_deve_conter_caracteres_especiais(cls, v):
    #     if special_c in v:
    #         raise ValueError('username should not contain special characs')
    #     return v

    @computed_field
    def username(self) -> str:
        return func_sanitiza(self.input_username)


class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class UsuarioUpdate(BaseModel):
    input_username: str = Field(alias='username')
    email: EmailStr | None = None
    senha: str | None = None

    # TODO: adicionar um validacao para caracteres especiais

    @computed_field
    def username(self) -> str:
        return func_sanitiza(self.input_username)


# Livro ---
class LivroSchema(BaseModel):
    input_titulo: str = Field(alias='titulo')
    ano: int = Field(gt=0, lt=dt.today().year)
    romancista_id: int

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
    id: int
    nome: str


# Token ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
