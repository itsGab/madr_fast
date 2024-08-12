from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Livro, Romancista, Usuario
from madr_fast.schemas import (
    LivroPublic,
    LivroSchema,
    LivroUpdate,
    Message,
    PaginaLivros,
)
from madr_fast.security import get_current_user

# rota
router = APIRouter(prefix='/livros', tags=['livros'])

# tipos annotated
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]

# configs para query (para definir paginacao)
offset_std = 0
limit_std = 20


# * CREATE ---
@router.post('/', response_model=LivroPublic, status_code=HTTPStatus.CREATED)
def cadastra_livro(
    livro: LivroSchema,
    session: T_Session,
    usuario_atual: T_CurrentUser,
):
    # verifica se o titulo do livro ja existe no banco de dados
    check_db = session.scalar(
        select(Livro).where(Livro.titulo == livro.titulo)
    )
    if check_db:  # caso exista, levanta conflict
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Livro já consta no MADR',
        )

    # verifica se o romancista existe no banco de dados
    check_romancista = session.scalar(
        select(Romancista).where(Romancista.id == livro.romancista_id)
    )
    if not check_romancista:
        raise HTTPException(  # caso romancista nao exista, levanta not found
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    # guarda os dados do livro no banco de dados
    livro_db = Livro(
        titulo=livro.titulo, ano=livro.ano, romancista_id=livro.romancista_id
    )
    session.add(livro_db)
    session.commit()
    session.refresh(livro_db)

    return livro_db


# * READ ---
# por id
@router.get(
    '/{livro_id}', response_model=LivroPublic, status_code=HTTPStatus.OK
)
def busca_livro_por_id(livro_id: int, session: T_Session):
    livro = session.scalar(select(Livro).where(Livro.id == livro_id))

    # verifica se existe livro com o livro_id
    if not livro:
        raise HTTPException(  # caso nao existe, levanta not found
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    return livro


# por query
@router.get(
    '/query/',
    response_model=PaginaLivros[LivroPublic],
    status_code=HTTPStatus.OK,
)
def busca_livros_por_query(
    session: T_Session,
    titulo: str = Query(None),
    ano: int = Query(None),
):
    # monta a query
    query = select(Livro)
    if titulo:
        query = query.filter(Livro.titulo.contains(titulo))
    if ano:
        query = query.filter(Livro.ano == ano)

    # retorna paginacao de livros
    return paginate(session, query=query)


@router.get(
    '/romancista/{romancista_id}',
    response_model=PaginaLivros[LivroPublic],
    status_code=HTTPStatus.OK,
)
def busca_livros_por_romancista_id(romancista_id: int, session: T_Session):
    # verifica se existe romancista no banco de dados
    check_romancista = session.scalar(
        select(Romancista).where(Romancista.id == romancista_id)
    )

    if not check_romancista:
        raise HTTPException(  # caso nao existe, levanta not found
            status_code=HTTPStatus.NOT_FOUND,
            detail='Romancista não consta no MADR',
        )

    query = select(Livro).filter(Livro.romancista_id == romancista_id)

    # retorna paginacao de livros
    return paginate(session, query=query)


# * UPDATE (PATCH) ---
@router.patch(
    '/{livro_id}', response_model=LivroPublic, status_code=HTTPStatus.OK
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
        raise HTTPException(  # caso nao existe, levanta not found
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    # verifica validade do titulo atualizado
    if livro_update.titulo and session.scalar(
        select(Livro).where(Livro.titulo == livro_update.titulo)
    ):
        raise HTTPException(  # caso ja exista, levanta conflict
            status_code=HTTPStatus.CONFLICT, detail='Título já consta no MADR'
        )

    # verifica se o romancista existe no banco de dados
    if livro_update.romancista_id:
        check_romancista = session.scalar(
            select(Romancista).where(
                Romancista.id == livro_update.romancista_id
            )
        )
        if not check_romancista:
            raise HTTPException(  # caso id nao exista, levanta not found
                status_code=HTTPStatus.NOT_FOUND,
                detail='Romancista não consta no MADR',
            )

    # atualiza os dados do livro para campos diferentes de None
    for chave, valor in livro_update.model_dump(exclude_none=True).items():
        setattr(livro_db, chave, valor)

    # atualiza o banco de dados
    session.add(livro_db)
    session.commit()
    session.refresh(livro_db)

    # retorna o livro atualizado
    return livro_db


# * DELETE ---
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
        raise HTTPException(  # se nao existir, levanta not found
            status_code=HTTPStatus.NOT_FOUND, detail='Livro não consta no MADR'
        )

    # deleta do banco de dados
    session.delete(livro_db)
    session.commit()

    # retorna mensagem de susseso
    return {'message': 'Livro deletado no MADR'}
