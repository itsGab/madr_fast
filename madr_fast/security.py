from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Annotated

from fastapi import Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session
from zoneinfo import ZoneInfo

from madr_fast.database import get_session
from madr_fast.models import Usuario
from madr_fast.schemas import TokenData
from madr_fast.settings import Settings

settings = Settings()
pwd_context = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/token', auto_error=False)
""" auto_error foi configurado para falso, para pegar o erro em execução e
retornar a exception em português. Segue documentação como informativo.

By default, if no HTTP Authorization header is provided, required for
    OAuth2 authentication, it will automatically cancel the request and
    send the client an error.

    If `auto_error` is set to `False`, when the HTTP Authorization header
    is not available, instead of erroring out, the dependency result will
    be `None`.

    This is useful when you want to have optional authentication.
"""

T_Token = Annotated[str, Depends(oauth2_scheme)]
T_Session = Annotated[Session, Depends(get_session)]


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({'exp': expire})
    encoded_jwt = encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_pwd: str, hashed_pwd: str):
    return pwd_context.verify(plain_pwd, hashed_pwd)


def get_current_user(
    session: T_Session,
    token: T_Token,
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Não autorizado',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if not username:
            raise credentials_exception
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception

    usuario = session.scalar(
        select(Usuario).where(Usuario.email == token_data.username)
    )

    if not usuario:
        raise credentials_exception
    return usuario
