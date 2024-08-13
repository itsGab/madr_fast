from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Romancista, Usuario
from madr_fast.schemas import (
    Message,
    PaginaRomancistas,
    RomancistaPublic,
    RomancistaSchema,
    RomancistaUpdate,
)
from madr_fast.security import get_current_user

router = APIRouter(prefix='/romancistas', tags=['Romancistas'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

# configs para query (para definir paginacao)
offset_std = 0
limit_std = 20


# * CREATE ---
@router.post(
    '/',
    response_model=RomancistaPublic,
    status_code=HTTPStatus.CREATED,
)
def cadastra_romancista(
    romancista: RomancistaSchema,
    session: T_Session,
    usuario_atual: T_CurrentUser,
):
    # verificar se o romancista existe no database
    check_db = session.scalar(
        select(Romancista).where(Romancista.nome == romancista.nome)
    )
    if check_db:
        raise HTTPException(  # caso exista, levanta conflict
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já consta no MADR',
        )

    # guarda dados do romancista no banco de dados
    romancista_db = Romancista(nome=romancista.nome)
    session.add(romancista_db)
    session.commit()
    session.refresh(romancista_db)

    return romancista_db


# * READ ---
# por id
@router.get('/{romancista_id}', response_model=RomancistaPublic)
def busca_romancistas_por_id(
    romancista_id: int,
    session: T_Session,
):
    # verifica se existe romancista por romancista_id
    romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )
    if not romancista:
        raise HTTPException(  # caso nao exista, levanta not found
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )
    return romancista


# por query
@router.get('/query/', response_model=PaginaRomancistas[RomancistaPublic])
def busca_romancistas_por_query(session: T_Session, nome: str = Query(None)):
    query = select(Romancista)

    # monta a query
    if nome:
        query = query.filter(Romancista.nome.contains(nome))

    # retorna paginacao de romancistas
    return paginate(session, query=query)


# * UPDATE (PATCH) ---
@router.patch(
    '/{romancista_id}',
    response_model=RomancistaPublic,
    status_code=HTTPStatus.OK,
)
def altera_romancista(
    romancista_id: int,
    session: T_Session,
    usuario_atual: T_CurrentUser,
    romancista_update: RomancistaUpdate,  # dados atualizados!!!
):
    # carrega o romancista por id do banco de dados
    romancista_db = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    # verifica se o romancista existe no banco de dados
    if not romancista_db:
        raise HTTPException(  # caso nao exista, levanta not found
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    # verifica validade do nome atualizado
    if romancista_update.nome and session.scalar(
        select(Romancista).where(Romancista.nome == romancista_update.nome)
    ):
        raise HTTPException(  # caso ja exista, levanta conflict
            status_code=HTTPStatus.CONFLICT, detail='Nome já consta no MADR'
        )

    # atualiza os dados do livro, caso diferente de None
    for chave, valor in romancista_update.model_dump(
        exclude_none=True
    ).items():
        setattr(romancista_db, chave, valor)

    # atualiza o banco de dados
    session.add(romancista_db)
    session.commit()
    session.refresh(romancista_db)

    # retorna o livro atualizado
    return romancista_db


# DELETE ---
@router.delete(
    '/{romancista_id}', response_model=Message, status_code=HTTPStatus.OK
)
def deleta_romancista(
    romancista_id: int,
    session: T_Session,
    usuario_atual: T_CurrentUser,
):
    # carrega o romancista buscado por id no banco de dados
    romancista_db = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    # verifica se o romancista existe no banco de dados
    if not romancista_db:
        # levanta a excecao NOT FOUND,
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    # deleta do banco de dados
    session.delete(romancista_db)
    session.commit()

    # retorna mensagem de sucesso
    return {'message': 'Romancista deletado no MADR'}
