from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Usuario
from madr_fast.schemas import (
    Message,
    UsuarioPublic,
    UsuarioSchema,
    UsuarioUpdate,
)
from madr_fast.security import get_current_user, get_password_hash

# rota
router = APIRouter(prefix='/contas', tags=['contas'])

# tipos annotated
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


# * CREATE ---
@router.post(
    '/', response_model=UsuarioPublic, status_code=HTTPStatus.CREATED
)
def registra_conta(usuario: UsuarioSchema, session: T_Session):
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
                detail='Conta já consta no MADR',
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


# * UPDATE ---
@router.put(
    '/{id_usuario}', response_model=UsuarioPublic, status_code=HTTPStatus.OK
)
def atualiza_conta(
    id_usuario: int,
    usuario: UsuarioUpdate,
    session: T_Session,
    usuario_atual: T_CurrentUser,
):
    if usuario_atual.id != id_usuario:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado'
        )

    usuario_db = session.scalar(
        select(Usuario).where(Usuario.id == id_usuario)
    )

    # verifica username ou email repetido
    check_db = session.scalar(
        select(Usuario).where(
            (
                (Usuario.username == usuario.username)
                & (Usuario.id != usuario_atual.id)
            )
            | (
                (Usuario.email == usuario.email)
                & (Usuario.id != usuario_atual.id)
            )
        )
    )
    if check_db:  # TODO: REDUNDANCIA, VERIFICAR COM CALMA
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Conta já consta no MADR',
        )

    if usuario.senha:
        usuario.senha = get_password_hash(usuario.senha)

    for chave, valor in usuario.model_dump(exclude_none=True).items():
        setattr(usuario_db, chave, valor)

    session.add(usuario_db)
    session.commit()
    session.refresh(usuario_db)

    return usuario_db


# * DELETE ---
@router.delete(
    '/{id_usuario}', response_model=Message, status_code=HTTPStatus.OK
)
def deleta_conta(
    id_usuario: int, session: T_Session, usuario_atual: T_CurrentUser
):
    if usuario_atual.id != id_usuario:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado'
        )

    session.delete(usuario_atual)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
