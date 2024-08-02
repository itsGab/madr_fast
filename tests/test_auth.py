from http import HTTPStatus


def test_pega_token(client, usuario):
    response = client.post(
        '/auth/token',
        data={'username': usuario.email, 'password': usuario.senha_pura},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'bearer'
