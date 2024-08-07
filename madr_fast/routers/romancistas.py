from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Romancista, Usuario
from madr_fast.schemas import (
    Message,
    RomancistaList,
    RomancistaResponse,
    RomancistaSchema,
    RomancistaUpdate,
)
from madr_fast.security import get_current_user

router = APIRouter(prefix='/romancistas', tags=['romancistas'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

# configs para query (para definir paginacao)
offset_std = 0
limit_std = 20


# CREATE ---
@router.post(
    '/',
    response_model=RomancistaResponse,
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
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Romancista já consta no MADR',
        )

    romancista_db = Romancista(nome=romancista.nome)
    (session.add(romancista_db),)
    session.commit()
    session.refresh(romancista_db)

    return romancista_db


# READ ---
# por id
@router.get('/{romancista_id}', response_model=RomancistaResponse)
def busca_romancistas_por_id(
    romancista_id: int,
    session: T_Session,
):
    romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )
    if not romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )
    return romancista


# por query
@router.get('/query/', response_model=RomancistaList)
def busca_romancistas_por_query(session: T_Session, nome: str = Query(None)):
    query = select(Romancista)

    if nome:
        query = query.filter(Romancista.nome.contains(nome))

    romancistas = session.scalars(
        query.offset(offset_std).limit(limit_std)
    ).all()

    return {'romancistas': romancistas}


# UPDATE (PATCH) ---
@router.patch(
    '/{romancista_id}',
    response_model=RomancistaResponse,
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
        # > levanta a excecao NOT FOUND < se nao existir
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    # verifica se o titulo do livro nao eh nulo (None) e
    # verifica se o novo nome do romancista causa CONFLITO (ja existe no db)
    if romancista_update.nome and session.scalar(
        select(Romancista).where(Romancista.nome == romancista_update.nome)
    ):
        raise HTTPException(
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
