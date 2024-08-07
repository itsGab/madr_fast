from datetime import datetime as dt

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    computed_field,
)


def func_sanitiza_espacos_e_minuscula(text):
    return ' '.join(text.lower().split())


# Message ---
class Message(BaseModel):
    message: str


# Usuario ---
class UsuarioSchema(BaseModel):
    input_username: str = Field(alias='username', min_length=1)
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
        return func_sanitiza_espacos_e_minuscula(self.input_username)


class UsuarioResponse(BaseModel):
    id: int
    username: str
    email: EmailStr


class UsuarioUpdate(BaseModel):
    input_username: str = Field(alias='username', default=None, min_length=1)
    email: EmailStr | None = None
    senha: str | None = None

    # TODO: adicionar um validacao para caracteres especiais

    @computed_field
    def username(self) -> str:
        if not self.input_username:
            return None
        return func_sanitiza_espacos_e_minuscula(self.input_username)


# Livro ---
class LivroSchema(BaseModel):
    input_titulo: str = Field(alias='titulo', min_length=1)
    ano: int = Field(gt=0, lt=dt.today().year + 1)
    romancista_id: int

    @computed_field
    def titulo(self) -> str:
        return func_sanitiza_espacos_e_minuscula(self.input_titulo)


class LivroResponse(LivroSchema):
    id: int


class LivroList(BaseModel):
    livros: list[LivroResponse]


class LivroUpdate(BaseModel):
    input_titulo: str | None = Field(
        alias='titulo', default=None, min_length=1
    )
    ano: int | None = Field(gt=0, lt=dt.today().year + 1, default=None)
    romancista_id: int | None = None

    @computed_field
    def titulo(self) -> str:
        if not self.input_titulo:
            return None
        return func_sanitiza_espacos_e_minuscula(self.input_titulo)


# Romancista ---
class RomancistaSchema(BaseModel):
    input_nome: str = Field(alias='nome', min_length=1)

    @computed_field
    def nome(self) -> str:
        return func_sanitiza_espacos_e_minuscula(self.input_nome)


class RomancistaResponse(RomancistaSchema):
    id: int


class RomancistaList(BaseModel):
    romancistas: list[RomancistaResponse]


class RomancistaUpdate(BaseModel):
    input_nome: str = Field(alias='nome', min_length=1)

    @computed_field
    def nome(self) -> str:
        return func_sanitiza_espacos_e_minuscula(self.input_nome)


# Token ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
