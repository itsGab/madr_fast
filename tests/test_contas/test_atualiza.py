from http import HTTPStatus

from sqlalchemy import select

from madr_fast.models import Usuario
from madr_fast.security import verify_password


def test_atualiza_valido_retorna_ok_e_schema(client, usuario, token):
    dados_atualizados = {
        'username': usuario.username,
        'email': 'atual@lizado.com',
        'senha': 'segredo',
    }
    output = {
        'username': usuario.username,
        'email': 'atual@lizado.com',
        'id': usuario.id,
    }

    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=dados_atualizados,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == output


def test_atualiza_com_token_invalido(client, usuario):
    dados_atualizados = {
        'username': 'atualizado',
        'email': 'atual@lizado.com',
        'senha': 'segredo',
    }

    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': 'Bearer token-invalido'},
        json=dados_atualizados,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_atualiza_por_usuario_invalido(client, outro_usuario, token):
    dados_atualizados = {
        'username': 'atualizado',
        'email': 'atual@lizado.com',
        'senha': 'segredo',
    }

    response = client.put(
        f'/contas/{outro_usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=dados_atualizados,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_atualiza_conflito_username_ja_existe(
    client, usuario, outro_usuario, token
):
    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': outro_usuario.username},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


def test_atualiza_conflito_email_ja_exite(
    client, usuario, outro_usuario, token
):
    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'email': outro_usuario.email},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


def test_atualiza_conflito_username_e_email_ja_existem(
    client, usuario, outro_usuario, token
):
    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': outro_usuario.username,
            'email': outro_usuario.email,
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


def test_atualiza_campos_em_branco_menos_username(client, usuario, token):
    # campo: username
    campo_atualizado = {'username': 'atualizado'}
    output = {
        'username': usuario.username,
        'email': usuario.email,
        'id': usuario.id,
    }
    output.update(campo_atualizado)

    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=campo_atualizado,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == output


def test_atualiza_campos_em_branco_menos_email(client, usuario, token):
    # campo: email
    campo_atualizado = {'email': 'atual@lizado.com'}
    output = {
        'username': usuario.username,
        'email': usuario.email,
        'id': usuario.id,
    }
    output.update(campo_atualizado)

    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=campo_atualizado,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == output


def test_atualiza_campos_em_branco_menos_senha(
    client, usuario, token, session
):
    # campo: senha
    campo_atualizado = {'senha': 'nova_senha'}
    output = {
        'username': usuario.username,
        'email': usuario.email,
        'id': usuario.id,
    }

    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=campo_atualizado,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == output

    # verifica senha
    dados = session.scalar(select(Usuario).where(Usuario.id == usuario.id))

    assert dados
    assert verify_password(campo_atualizado['senha'], dados.senha)


def test_atualiza_username_sanitizado(client, usuario, token):
    username_com_espacos = '   uSer      NamE     '
    output = {
        'username': 'user name',  # username esperado
        'email': usuario.email,
        'id': usuario.id,
    }

    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'username': username_com_espacos},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == output


def test_atualiza_email_invalido(client, usuario, token):
    email_invalido = 'email-invalido'

    response = client.put(
        f'/contas/{usuario.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'email': email_invalido},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg'] == 'value is not a valid email'
        ' address: An email address must have an @-sign.'
    )
