from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Livro, Romancista, Usuario
from madr_fast.schemas import LivroResponse, LivroSchema
from madr_fast.security import get_current_user

router = APIRouter(prefix='/livros', tags=['livros'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


# CREATE ---
@router.post('/', response_model=LivroResponse, status_code=HTTPStatus.CREATED)
def cadastrar_livro(
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
# read list?

# UPDATE (PATCH) ---

# DELETE ---
