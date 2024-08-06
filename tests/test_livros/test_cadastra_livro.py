from http import HTTPStatus


def test_cadastra_livro_retorno_criado_e_schema(client, romancista, token):
    json_input = {
        'titulo': 'livro de teste',
        'ano': 1999,
        # deve ter romancista_id criado para nao dar erro
        'romancista_id': romancista.id,
    }

    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'titulo': 'livro de teste',
        'ano': 1999,
        'romancista_id': romancista.id,
        'id': 1,
    }


def test_cadastra_livro_sem_autenticacao_retorna_nao_autorizado(
    client, romancista
):
    json_input = {
        'titulo': 'livro de teste',
        'ano': 1999,
        'romancista_id': romancista.id,
    }

    response = client.post(
        '/livros',
        headers={'Authorization': 'Bearer token-invalido'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_cadastra_livro_retorna_nome_sanitizado(client, romancista, token):
    json_input = {
        'titulo': '    LivRo  SanitiZAdo    ',
        'ano': 1999,
        'romancista_id': romancista.id,
    }

    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'titulo': 'livro sanitizado',
        'ano': 1999,
        'romancista_id': romancista.id,
        'id': 1,
    }


def test_cadastra_livro_ja_cadastrado_retorna_conflito(client, livro, token):
    json_input = {
        'titulo': livro.titulo,
        'ano': 1999,
        'romancista_id': livro.romancista_id,
    }

    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert livro.titulo == 'o ultimo romantico'
    assert response.json() == {'detail': 'Livro já consta no MADR'}
    assert response.status_code == HTTPStatus.CONFLICT


def test_cadastra_livro_sem_romancista_id_valido_retorna_erro(
    client, romancista, token
):
    json_input = {
        'titulo': 'livro de teste',
        'ano': 1999,
        'romancista_id': None,
    }

    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg']
        == 'Input should be a valid integer'
    )


def test_cadastra_livro_romancista_id_nao_cadastrado_retorna_erro(
    client, romancista, token
):
    json_input = {
        'titulo': 'livro de teste',
        'ano': 1999,
        'romancista_id': 2,
    }

    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_cadastra_livro_nome_str_vazia_retorna_erro(client, token, romancista):
    json_input = {
        'titulo': '',
        'ano': 1999,
        'romancista_id': romancista.id,
    }

    response = client.post(
        '/livros',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg']
        == 'String should have at least 1 character'
    )
