from http import HTTPStatus

from freezegun import freeze_time

freeze_time()


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


def test_auth_token_expirado(client, usuario):
    with freeze_time('2024-01-01 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': usuario.email, 'password': usuario.senha_pura},
        )
        token = response.json()['access_token']

    assert response.status_code == HTTPStatus.OK
    assert token

    # após 61 minutos: expirado
    with freeze_time('2024-01-01 13:01:00'):
        response = client.put(
            f'/contas/{usuario.id}',
            headers={'Authorization': f'Bearer {token}'},
            json={
                'username': 'token expirado',
                'email': 'token@exp.com',
                'senha': 'segredo',
            },
        )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_auth_atualiza_token_retorna_ok_e_token_de_acesso(client, token):
    response = client.post(
        '/auth/refresh_token', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in response.json()
    assert response.json()['token_type'] == 'bearer'


def test_auth_atualiza_token_token_expirado_retorno_erro(client, usuario):
    with freeze_time('2024-01-01 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': usuario.email, 'password': usuario.senha_pura},
        )
        token = response.json()['access_token']

    assert response.status_code == HTTPStatus.OK
    assert token

    # após 61 minutos: expirado
    with freeze_time('2024-01-01 13:01:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_auth_atualiza_token_sem_token(client):
    response = client.post(
        '/auth/refresh_token',
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}
