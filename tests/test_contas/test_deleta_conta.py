from http import HTTPStatus


def test_deleta_valido_retorna_ok_e_message(client, usuario):
    response = client.post(
        '/auth/token',
        data={'username': usuario.email, 'password': usuario.senha_pura},
    )
    token = response.json()['access_token']
    assert token

    response = client.delete(
        f'/contas/{usuario.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Conta deletada com sucesso'}


def test_deleta_sem_token(client, usuario):
    response = client.delete(
        f'/contas/{usuario.id}',
        headers={},  # sem token
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_deleta_token_invalido(client, usuario):
    response = client.delete(
        f'/contas/{usuario.id}',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_deleta_por_usuario_invalido(client, usuario, outro_usuario):
    response = client.post(
        '/auth/token',
        data={
            'username': outro_usuario.email,
            'password': outro_usuario.senha_pura,
        },
    )
    token = response.json()['access_token']
    assert token

    response = client.delete(
        f'/contas/{usuario.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}
