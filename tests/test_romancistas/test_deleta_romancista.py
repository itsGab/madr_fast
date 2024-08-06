from http import HTTPStatus


def test_deleta_romancista_retorna_ok_e_message(client, romancista, token):
    response = client.delete(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado no MADR'}


def test_deleta_romancista_sem_autenticacao_retorna_nao_autorizado(
    client, romancista
):
    response = client.delete(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Não autorizado'}


def test_deleta_romancista_id_nao_cadastrado_retorna_erro(
    client, romancista, token
):
    response = client.delete(
        f'/romancistas/{romancista.id + 1}',  # id nao cadastrado
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}
