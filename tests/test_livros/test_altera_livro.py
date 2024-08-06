from datetime import datetime as dt
from http import HTTPStatus


def test_altera_livro_retorna_ok_e_schema(
    client, livro, token, outro_romancista
):
    json_input = {
        'titulo': 'titulo atualizado',
        'ano': 2024,
        'romancista_id': outro_romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    json_output = {
        'titulo': 'titulo atualizado',
        'ano': 2024,
        'romancista_id': outro_romancista.id,
        'id': livro.id,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_output


def test_altera_livro_sem_autentificacao_retorna_nao_autorizado(
    client, livro, romancista
):
    json_input = {
        'titulo': 'titulo atualizado',
        'ano': 2024,
        'romancista_id': romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': 'Bearer token-invalido'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_altera_livro_titulo_sanitizado_retorna_ok_e_titulo_sanitizado(
    client, livro, romancista, token
):
    json_input = {
        'titulo': '   TiTuLO     SAniTIzaDO    ',
        'ano': 2024,
        'romancista_id': romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    json_output = {
        'titulo': 'titulo sanitizado',
        'ano': 2024,
        'romancista_id': romancista.id,
        'id': livro.id,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_output


def test_altera_livro_id_nao_cadastrado_retorna_erro(
    client, livro, romancista, token
):
    json_input = {
        'titulo': 'titulo atualizado',
        'ano': 2024,
        'romancista_id': romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_altera_livro_titulo_ja_existe_retorna_conflito(
    client, livro, outro_livro, romancista, token
):
    json_input = {
        'titulo': outro_livro.titulo,
        'ano': 2024,
        'romancista_id': romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {'detail': 'Título já consta no MADR'}


def test_altera_livro_todos_campos_vazios_menos_titulo(
    client, livro, token, romancista
):
    json_input = {
        'titulo': 'titulo atualizado',
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    json_output = {
        'titulo': 'titulo atualizado',
        'ano': livro.ano,
        'romancista_id': romancista.id,
        'id': livro.id,
    }

    assert response.json() == json_output
    assert response.status_code == HTTPStatus.OK


def test_altera_livro_todos_campos_vazios_menos_ano(
    client, livro, token, romancista
):
    json_input = {
        'ano': 2024,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    json_output = {
        'titulo': livro.titulo,
        'ano': 2024,
        'romancista_id': romancista.id,
        'id': livro.id,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_output


def test_altera_livro_todos_campos_vazios_menos_romancista_id(
    client, livro, token, outro_romancista
):
    json_input = {'romancista_id': outro_romancista.id}

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    json_output = {
        'titulo': livro.titulo,
        'ano': livro.ano,
        'romancista_id': outro_romancista.id,
        'id': livro.id,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json() == json_output


def test_altera_livro_limites_campo_ano(
    # limite inferior (ano deve ser maior que 0)
    client,
    livro,
    token,
    outro_romancista,
):
    json_input = {
        'titulo': 'titulo atualizado',
        'ano': 0,
        'romancista_id': outro_romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg'] == 'Input should be greater than 0'
    )

    # limite superior (ano deve ser menor que ano atual + 1)
    json_input = {
        'titulo': 'titulo atualizado',
        'ano': dt.today().year + 1,
        'romancista_id': outro_romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        response.json()['detail'][0]['msg'] == 'Input should be less than 2025'
    )


def test_altera_livro_str_no_campo_ano_retorna_ano_inteiro(
    # limite inferior (ano deve ser maior que 0)
    client,
    livro,
    token,
    outro_romancista,
):
    # erro: str no lugar de int
    json_input = {
        'titulo': 'titulo atualizado',
        'ano': '2017',
        'romancista_id': outro_romancista.id,
    }

    response = client.patch(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
        json=json_input,
    )

    ano_intenger = 2017

    assert response.status_code == HTTPStatus.OK
    assert response.json()['ano'] == ano_intenger
    assert isinstance(response.json()['ano'], int)
