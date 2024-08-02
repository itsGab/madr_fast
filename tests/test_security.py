from jwt import decode

from madr_fast.security import (
    create_access_token,
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
