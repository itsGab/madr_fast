from http import HTTPStatus


def test_cadastra_romancista_retorna_criado_e_schema(client, token):
    json_input = {'nome': 'nome teste do romancista'}

    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'nome': 'nome teste do romancista',
        'id': 1,
    }


def test_cadastra_romancista_sem_autenticacao_retorna_nao_autorizado(client):
    json_input = {'nome': 'nome teste do romancista'}

    response = client.post(
        '/romancistas',
        headers={'Authorization': 'Bearer token-invalido'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_cadastra_romancista_retorna_nome_sanitizado(client, token):
    json_input = {'nome': '     rOMANcista   SanitIzADO    '}

    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'nome': 'romancista sanitizado',
        'id': 1,
    }


def test_cadastra_romancista_ja_cadastrado_retorna_conflito(
    client, romancista, token
):
    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json={'nome': romancista.nome},
    )

    assert romancista.nome == 'jorge'
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Romancista já consta no MADR'}


def test_cadastra_romanicsta_nome_str_vazia_retorna_erro(client, token):
    json_input = {'nome': ''}

    response = client.post(
        '/romancistas',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg']
        == 'String should have at least 1 character'
    )
