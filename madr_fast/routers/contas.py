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
router = APIRouter(prefix='/contas', tags=['Contas'])

# tipos annotated
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


# * CREATE ---
@router.post('/', response_model=UsuarioPublic, status_code=HTTPStatus.CREATED)
def registra_conta(usuario: UsuarioSchema, session: T_Session):
    # verifica se ja existe usuario com mesmo username ou email
    check_db = session.scalar(
        select(Usuario).where(
            (Usuario.username == usuario.username)
            | (Usuario.email == usuario.email)
        )
    )
    if check_db:
        raise HTTPException(  # caso existe, levanta conflict
            status_code=HTTPStatus.CONFLICT,
            detail='Conta já consta no MADR',
        )

    # caso nao exista, criptografa a senha e adicona ao banco de dados
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
    usuario_atualiza: UsuarioUpdate,  # novos dados para atualizacao
    session: T_Session,
    usuario_atual: T_CurrentUser,
):
    # verifica se o atual eh diferente do usuario sendo alterado
    if usuario_atual.id != id_usuario:
        raise HTTPException(  # caso usuario diferente, levanta unathorized
            status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado'
        )

    # pegas os dados do usuario no banco de dados
    usuario_db = session.scalar(
        select(Usuario).where(Usuario.id == id_usuario)
    )

    # verifica username ou email de atualizacao nao existem no banco de dados
    check_db = session.scalar(
        select(Usuario).where(
            (  # condicoes levam em conta o id do usuario
                (Usuario.username == usuario_atualiza.username)
                & (Usuario.id != usuario_atual.id)
            )
            | (
                (Usuario.email == usuario_atualiza.email)
                & (Usuario.id != usuario_atual.id)
            )
        )
    )
    if check_db:
        raise HTTPException(  # caso existam, levanta conflict
            status_code=HTTPStatus.CONFLICT,
            detail='Username ou e-mail já consta no MADR',
        )

    # caso seja atualizada a senha, gera nova senha criptografada
    if usuario_atualiza.senha:
        usuario_atualiza.senha = get_password_hash(usuario_atualiza.senha)

    # atualiza os dados do usuario caso sejam diferente de none
    for chave, valor in usuario_atualiza.model_dump(exclude_none=True).items():
        setattr(usuario_db, chave, valor)

    # adiciona os dados atualizados ao banco de dados
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
    # verifica se o atual eh diferente do usuario sendo deletado
    if usuario_atual.id != id_usuario:
        raise HTTPException(  # caso usuario diferente, levanta unathorized
            status_code=HTTPStatus.UNAUTHORIZED, detail='Não autorizado'
        )

    # remove os usuario do banco de dados
    session.delete(usuario_atual)
    session.commit()

    return {'message': 'Conta deletada com sucesso'}
