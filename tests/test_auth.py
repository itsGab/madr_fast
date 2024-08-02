from http import HTTPStatus


def test_auth_token_retorna_ok_e_token_de_acesso(client, usuario):
    response = client.post(
        '/auth/token',
        data={'username': usuario.email, 'password': usuario.senha_pura},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert token['token_type'] == 'bearer'


def test_auth_token_login_invalido(client, usuario):
    # faltando username
    response = client.post(
        '/auth/token',
        data={
            'username': 'email-errado@de.teste',
            'password': usuario.senha_pura,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}

    # faltando senha
    response = client.post(
        '/auth/token',
        data={'username': usuario.email, 'password': 'segredo-errado'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email ou senha incorretos'}


def test_auth_token_expirado(): ...


def test_auth_atualiza_token_retorna_ok_e_token_de_acesso(): ...


def test_auth_atualiza_token_token_expirado_retorno_erro(): ...
