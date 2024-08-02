from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Usuario
from madr_fast.schemas import UsuarioResponse, UsuarioSchema, UsuarioUpdate
from madr_fast.security import get_password_hash, get_current_user, settings

router = APIRouter(prefix='/contas', tags=['contas'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


@router.post(
    '/', response_model=UsuarioResponse, status_code=HTTPStatus.CREATED
)
def cria_conta(usuario: UsuarioSchema, session: T_Session):
    usuario_db = session.scalar(
        select(Usuario).where(
            (Usuario.username == usuario.username)
            | (Usuario.email == usuario.email)
        )
    )

    if usuario_db:
        if (
            usuario_db.username == usuario.username
            or usuario_db.email == usuario.email
        ):
            raise HTTPException(  # TODO: melhorar exception
                status_code=HTTPStatus.CONFLICT,
                detail='conta já consta no MADR',
            )

    hash_da_senha = get_password_hash(usuario.senha)

    usuario_db = Usuario(
        username=usuario.username,
        senha=hash_da_senha,
        email=usuario.email,
    )
    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)

    return usuario_db


@router.put(
    '/{id_usuario}', response_model=UsuarioResponse, status_code=HTTPStatus.OK
)
def atualiza_conta(
    id_usuario, 
    usuario: UsuarioUpdate, 
    session: T_Session,
    usuario_atual: T_CurrentUser
):
    if usuario_atual.id != id_usuario:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Não autorizado'
        )

    usuario_atual = session.scalar(
        select(Usuario).where((Usuario.id == id_usuario))
    )
    for key, value in usuario.model_dump(exclude_unset=True).items():
        setattr(usuario_atual, key, value)

    session.add(usuario_atual)
    session.commit()
    session.refresh(usuario_atual)

    return usuario_atual
