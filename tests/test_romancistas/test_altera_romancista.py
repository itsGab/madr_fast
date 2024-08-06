from http import HTTPStatus


def test_altera_romancista_retorna_ok_e_schema(client, romancista, token):
    json_input = {
        'nome': 'jorge da silva',
    }

    response = client.patch(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    json_output = {'nome': 'jorge da silva', 'id': romancista.id}

    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_output


def test_altera_romancista_sem_autenticacao_retorna_nao_autorizado(
    client, romancista
):
    json_input = {
        'nome': 'jorge da silva',
    }

    response = client.patch(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': 'Bearer token-invalido'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


# AQUI
def test_altera_romancista_nome_sanitizado_retorna_ok_e_nome_sanitizado(
    client, romancista, token
):
    json_input = {
        'nome': '    JORGE    da    silvA    ',
    }

    response = client.patch(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    json_output = {'nome': 'jorge da silva', 'id': romancista.id}

    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_output


def test_altera_romancista_id_nao_cadastrado_retorna_erro(
    client, romancista, token
):
    json_input = {
        'nome': 'jorge da silva',
    }

    response = client.patch(
        f'/romancistas/{romancista.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_altera_romancista_nome_ja_existe_retorna_conflito(
    client, romancista, token
):
    json_input = {
        'nome': romancista.nome,
    }

    response = client.patch(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Nome já consta no MADR'}


def test_altera_romancista_campo_nome_str_vazia_retorna_erro(  # `nome = ''`
    client, romancista, token
):
    json_input = {
        'nome': '',
    }

    response = client.patch(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg']
        == 'String should have at least 1 character'
    )
