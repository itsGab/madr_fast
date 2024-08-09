from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Livro, Romancista, Usuario
from madr_fast.schemas import (
    LivroList,
    LivroResponse,
    LivroSchema,
    LivroUpdate,
    Message,
)
from madr_fast.security import get_current_user

router = APIRouter(prefix='/livros', tags=['livros'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

# configs para query (para definir paginacao)
offset_std = 0
limit_std = 20


# CREATE ---
@router.post('/', response_model=LivroResponse, status_code=HTTPStatus.CREATED)
def cadastra_livro(
    livro: LivroSchema,
    session: T_Session,
    usuario_atual: T_CurrentUser,
):
    # verificar por titulo se o livro ja existe no database
    check_db = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )
    if check_db:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Livro já consta no MADR',
        )

    # verificar se o romancista NÃO existe no database
    check_romancista = session.scalar(
        select(Romancista).where(Romancista.id == livro.romancista_id)
    )
    if not check_romancista:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,  # Será BAD_REQUEST ???
            detail='Romancista não consta no MADR',
        )

    livro_db = Livro(
        titulo=livro.titulo, ano=livro.ano, romancista_id=livro.romancista_id
    )
    session.add(livro_db)
    session.commit()
    session.refresh(livro_db)

    return livro_db


# READ ---
# read por id
@router.get(
    '/{livro_id}', response_model=LivroResponse, status_code=HTTPStatus.OK
)
def busca_livro_por_id(livro_id: int, session: T_Session):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    if not livro:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    return livro


# read por query
@router.get('/query/', response_model=LivroList, status_code=HTTPStatus.OK)
def busca_livros_por_query(
    session: T_Session,
    titulo: str = Query(None),
    ano: int = Query(None),
):
    query = select(Livro)

    if titulo:
        query = query.filter(Livro.titulo.contains(titulo))
    if ano:
        query = query.filter(Livro.ano == ano)

    livros = session.scalars(query.offset(offset_std).limit(limit_std)).all()

    # if not livros:
    #     raise HTTPException(
    #         status_code=HTTPStatus.NOT_FOUND,
    #         detail='Livros não constam no MADR',
    #     )

    return {'livros': livros}


#  TODO: Implementar GET de livro por romancista_id !!!
@router.get(
    '/por_romancista/{romancista_id}',
    response_model=LivroList,
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
def busca_por_romancista_id(): ...


# UPDATE (PATCH) ---
@router.patch(
    '/{livro_id}', response_model=LivroResponse, status_code=HTTPStatus.OK
)
def altera_livro(
    livro_id: int,
    session: T_Session,
    usuario_atual: T_CurrentUser,
    livro_update: LivroUpdate,  # dados atualizados!!!
):
    # carrega o livro buscado por id do banco de dados
    livro_db = session.scalar(select(Livro).where(Livro.id == livro_id))

    # verifica se o livro existe no banco de dados
    if not livro_db:
        # > levanta a excecao NOT FOUND < se nao existir
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    # verifica se o titulo do livro nao eh nulo (None) e
    # verifica se o novo titulo causa CONFLITO (se ja existe um cadastro dele)
    if livro_update.titulo and session.scalar(
        select(Livro).where(Livro.titulo == livro_update.titulo)
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail='Título já consta no MADR'
        )

    # atualiza os dados do livro, caso diferente de None
    for chave, valor in livro_update.model_dump(exclude_none=True).items():
        setattr(livro_db, chave, valor)

    # atuailiza o banco de dados
    session.add(livro_db)
    session.commit()
    session.refresh(livro_db)

    # retorna o livro atualizado
    return livro_db


# DELETE ---
@router.delete(
    '/{livro_id}', response_model=Message, status_code=HTTPStatus.OK
)
def deleta_livro(
    livro_id: int,
    session: T_Session,
    usuario_atual: T_CurrentUser,
):
    # carrega o livro buscado por id no banco de dados
    livro_db = session.scalar(select(Livro).where(Livro.id == livro_id))

    # verifica se o livro existe no banco de dados
    if not livro_db:
        # levanta a excecao NOT FOUND
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    # deleta do banco de dados
    session.delete(livro_db)
    session.commit()

    # retorna mensagem de susseso
    return {'message': 'Livro deletado no MADR'}
