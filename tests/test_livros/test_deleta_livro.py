from http import HTTPStatus


def test_deleta_livro_retorna_ok_e_message(client, livro, token):
    response = client.delete(
        f'/livros/{livro.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Livro deletado no MADR'}


def test_deleta_livro_sem_autenticacao_retorna_nao_autorizado(client, livro):
    response = client.delete(
        f'/livros/{livro.id}',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_deleta_livro_id_nao_cadastrado_retorna_erro(client, livro, token):
    response = client.delete(
        f'/livros/{livro.id + 1}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}
