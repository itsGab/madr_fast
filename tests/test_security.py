import pytest
from fastapi.exceptions import HTTPException
from jwt import decode

from madr_fast.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    settings,
    verify_password,
)


def test_pwds():
    segredo = 'segredo'
    segredo_hashed = get_password_hash(segredo)
    assert verify_password(segredo, segredo_hashed)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)
    decoded = decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert decoded['test'] == data['test']
    assert decoded['exp']


def test_security_current_user_token_invalido(session):
    # test case for JWT token error (or decode error)
    with pytest.raises(HTTPException):
        get_current_user(session, token='invalid-token')


def test_security_current_user_token_vazio(session):
    # test case for user not found in the database
    data_no_username = {'sub': 'test@test'}
    token = create_access_token(data_no_username)

    with pytest.raises(HTTPException):
        get_current_user(session, token)


def test_security_current_user_token_sem_sub(session):
    # test case for missing 'sub' in the payload
    data_user_none = {'test': 'test'}
    token = create_access_token(data_user_none)

    with pytest.raises(HTTPException):
        get_current_user(session, token)
