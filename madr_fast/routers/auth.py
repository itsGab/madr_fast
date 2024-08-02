from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from madr_fast.database import get_session
from madr_fast.models import Usuario
from madr_fast.schemas import Token
from madr_fast.security import (
    create_access_token,
    # get_password_hash,
    verify_password,
    get_current_user,
)

router = APIRouter(prefix='/auth', tags=['auth'])

# types annotated
T_FormData = Annotated[OAuth2PasswordRequestForm, Depends()]
T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[Usuario, Depends(get_current_user)]


@router.post('/token', response_model=Token)
def login_para_token_de_acesso(form_data: T_FormData, session: T_Session):
    usuario_db = session.scalar(
        select(Usuario).where(Usuario.email == form_data.username)
    )

    if not usuario_db:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorretos',
        )
    if not verify_password(form_data.password, usuario_db.senha):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Email ou senha incorretos',
        )
    token_de_acesso = create_access_token(data={'sub': usuario_db.email})
    return {'access_token': token_de_acesso, 'token_type': 'bearer'}


@router.post('/refresh_token', response_model=Token)
def atualiza_token_de_acesso(usuario_atual: T_CurrentUser):
    novo_token_de_acesso = create_access_token(
        data={'sub': usuario_atual.email}
    )
    
    return {'access_token': novo_token_de_acesso, 'token_type': 'bearer'}
