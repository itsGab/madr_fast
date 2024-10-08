import re
from datetime import datetime as dt
from typing import TypeVar

from fastapi_pagination import Page
from fastapi_pagination.customization import (
    CustomizedPage,
    UseFieldsAliases,
    UseName,
    UseParamsFields,
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
)


# * Função de validação e sanitização usada nas entradas de texto
def valida_e_sanitiza(text):
    if re.search(r'[^\w\s\à-ÿÀ-Ÿ]', text, re.UNICODE):
        raise ValueError('entrada deve conter apenas letras e números')
    return ' '.join(text.lower().split())


# * Paginação ---
tamanho_pagina = 20  # itens
T = TypeVar('T')

PaginaLivros = CustomizedPage[
    Page[T],
    UseName('PaginaLivros'),
    UseParamsFields(size=tamanho_pagina),
    UseFieldsAliases(
        items='livros',
        page='página',
        size='tamanho',
        pages='páginas',
    ),
]

PaginaRomancistas = CustomizedPage[
    Page[T],
    UseName('PaginaRomancistas'),
    UseParamsFields(size=tamanho_pagina),
    UseFieldsAliases(
        items='romancistas',
        page='página',
        size='tamanho',
        pages='páginas',
    ),
]


# * Message ---
class Message(BaseModel):
    message: str


# * Usuario ---
class UsuarioSchema(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    senha: str

    _valida_e_sanitiza = field_validator('username')(valida_e_sanitiza)


class UsuarioPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UsuarioUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    senha: str | None = None

    _valida_e_sanitiza = field_validator('username')(valida_e_sanitiza)


# * Livro ---
class LivroSchema(BaseModel):
    titulo: str = Field(min_length=1)
    ano: int = Field(gt=0, lt=dt.today().year + 1)
    romancista_id: int

    _valida_e_sanitiza = field_validator('titulo')(valida_e_sanitiza)


class LivroPublic(LivroSchema):
    id: int


class LivroUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1)
    ano: int | None = Field(gt=0, lt=dt.today().year + 1, default=None)
    romancista_id: int | None = None

    _valida_e_sanitiza = field_validator('titulo')(valida_e_sanitiza)


# * Romancista ---
class RomancistaSchema(BaseModel):
    nome: str = Field(min_length=1)

    _valida_e_sanitiza = field_validator('nome')(valida_e_sanitiza)


class RomancistaPublic(RomancistaSchema):
    id: int


class RomancistaUpdate(BaseModel):
    nome: str = Field(min_length=1)

    _valida_e_sanitiza = field_validator('nome')(valida_e_sanitiza)


# * Token ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
