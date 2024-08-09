from http import HTTPStatus

from tests.factories import RomancistaFactory


def test_busca_romancista_por_id_retorna_ok_e_schema(client, romancista):
    response = client.get(
        f'/romancistas/{romancista.id}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'id': romancista.id, 'nome': romancista.nome}


def test_busca_romancista_por_id_id_nao_cadastrado_retorna_erro(
    client, romancista
):
    response = client.get(
        f'/romancistas/{romancista.id + 1}',
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Romancista não consta no MADR'}


def test_busca_romancista_por_query_filtra_nome_parcial_retorna_lista(
    client, romancista, outro_romancista
):
    nome_parcial = romancista.nome[0:2]
    response = client.get(
        f'/romancistas/query/?nome={nome_parcial}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'romancistas': [{'id': romancista.id, 'nome': romancista.nome}]
    }


def test_busca_romancista_por_query_deve_retorna_paginacao_maiores_que_20(
    client, session
):
    # factory
    session.bulk_save_objects(RomancistaFactory.create_batch(25))

    response = client.get(
        '/romancistas/query/',
    )

    limite_por_pagina = 20
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['romancistas']) == limite_por_pagina


def test_busca_romancista_por_query_vazias_retorna_lista_total(
    client, session
):
    # factory
    session.bulk_save_objects(RomancistaFactory.create_batch(7))

    response = client.get(
        '/romancistas/query/',
    )

    numero_total_de_registro = 7
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['romancistas']) == numero_total_de_registro


def test_busca_romancista_por_query_sem_correspondencia_retorna_lista_vazia(
    client, romancista, outro_romancista
):
    nome_sem_correspondencia = 'semcorrespondencia'
    response = client.get(
        f'/romancistas/query/?nome={nome_sem_correspondencia}',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'romancistas': []}
