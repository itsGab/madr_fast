from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Romancista, Usuario
from madr_fast.schemas import RomancistaResponse, RomancistaSchema
from madr_fast.security import get_current_user

router = APIRouter(prefix='/romancistas', tags=['romancistas'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


# CREATE ---
@router.post(
    '/',
    response_model=RomancistaResponse,
    status_code=HTTPStatus.CREATED,
)
def cadastrar_romancista(
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
# read list?

# UPDATE (PATCH) ---

# DELETE ---
