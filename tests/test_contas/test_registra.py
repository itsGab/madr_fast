from http import HTTPStatus

from sqlalchemy import select

from madr_fast.models import Usuario
from madr_fast.security import verify_password


def test_registra_valido_retorna_criado_e_schema(client):
    # data
    json_input = {
        'username': 'teste-usuario',
        'email': 'usuario@de.teste',
        'senha': 'segredo-de-usuario',
    }
    json_output = {  # saida esperada
        'username': 'teste-usuario',
        'email': 'usuario@de.teste',
        'id': 1,
    }

    response = client.post('/contas', json=json_input)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == json_output


def test_registra_senha_criptografada(client, session):
    json_input = {
        'username': 'teste-senha',
        'email': 'senha@de.teste',
        'senha': 'segredo-de-senha',
    }
    client.post('/contas', json=json_input)

    usuario_db = session.scalar(
        select(Usuario).where(Usuario.username == json_input['username'])
    )
    senha_db = usuario_db.senha
    senha_pura = json_input['senha']

    assert senha_db != senha_pura
    assert verify_password(senha_pura, senha_db)


def test_registra_conflito_dados_ja_existem(client):
    json_input = {
        'username': 'teste-conflito',
        'email': 'conflito@de.teste',
        'senha': 'segredo-de-conflito',
    }
    json_output = {
        'username': 'teste-conflito',
        'email': 'conflito@de.teste',
        'id': 1,
    }

    response = client.post('/contas', json=json_input)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == json_output

    # conflito: username repetido
    json_input_username_repetido = {
        'username': 'teste-conflito',  # repetido
        'email': 'username-repetido@de.teste',
        'senha': 'segredo-de-username-repetido',
    }

    response = client.post('/contas', json=json_input_username_repetido)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}

    # conflito: email repetido
    json_input_email_repetido = {
        'username': 'teste-email-repetido',
        'email': 'conflito@de.teste',  # repetido
        'senha': 'segredo-de-email-repetido',
    }

    response = client.post('/contas', json=json_input_email_repetido)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Conta já consta no MADR'}


def test_registra_username_sanitizado(client):
    json_input = {
        'username': '    DEVE  SER   sanitiZado    ',
        'email': 'sanitizado@de.teste',
        'senha': 'segredo-de-sanitizado',
    }
    json_output = {
        'username': 'deve ser sanitizado',
        'email': 'sanitizado@de.teste',
        'id': 1,
    }
    response = client.post('/contas', json=json_input)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == json_output


def test_registra_email_invalido_IMPLEMENTAR(client):
    json_input = {
        'username': 'user-test',
        'email': 'email-invalido',
        'senha': 'segredo',
    }

    response = client.post(
        '/contas',
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg'] == 'value is not a valid email'
        ' address: An email address must have an @-sign.'
    )
