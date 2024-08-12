from http import HTTPStatus

from sqlalchemy import select

from madr_fast.models import Livro
from tests.factories import LivroFactory


def test_busca_livro_por_id_retorna_ok_e_schema(client, outro_livro, livro):
    response = client.get(f'/livros/{livro.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': livro.id,
        'titulo': livro.titulo,
        'ano': livro.ano,
        'romancista_id': livro.romancista_id,
    }


def test_busca_livro_por_id_id_nao_cadastrado_retorna_erro(client, livro):
    response = client.get(f'/livros/{livro.id + 1}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Livro não consta no MADR'}


def test_busca_livro_por_query_filtra_nome_parcial_retorna_lista(
    client, outro_livro, livro
):
    titulo_parcial = livro.titulo[:5]
    outro_titulo = outro_livro.titulo

    assert titulo_parcial not in outro_titulo

    response = client.get(f'/livros/query/?titulo={titulo_parcial}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'livros': [
            {
                'id': livro.id,
                'titulo': livro.titulo,
                'ano': livro.ano,
                'romancista_id': livro.romancista_id,
            }
        ]
    }


def test_busca_livro_por_query_filtra_ano_retorna_lista(
    client, session, romancista
):
    ano_alvo = 2001
    num_livros_alvo = 5
    # factory
    session.bulk_save_objects(
        LivroFactory.create_batch(3, ano=1999, romancista_id=romancista.id)
    )
    session.bulk_save_objects(
        LivroFactory.create_batch(
            num_livros_alvo, ano=ano_alvo, romancista_id=romancista.id
        )
    )

    response = client.get(f'/livros/query/?ano={2001}')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == num_livros_alvo


def test_busca_livro_por_query_filtra_combinado_retorna_lista(
    client, session, livro, romancista
):
    # factory
    session.bulk_save_objects(
        LivroFactory.create_batch(3, ano=2000, romancista_id=romancista.id)
    )
    session.bulk_save_objects(
        LivroFactory.create_batch(5, ano=2001, romancista_id=romancista.id)
    )

    response = client.get(
        f'/livros/query/?titulo={livro.titulo}&ano={livro.ano}'
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'livros': [
            {
                'id': livro.id,
                'titulo': livro.titulo,
                'ano': livro.ano,
                'romancista_id': livro.romancista_id,
            }
        ]
    }


def test_busca_livro_por_query_deve_retorna_paginacao_maiores_que_20(
    client, session, romancista
):
    # factory
    session.bulk_save_objects(
        LivroFactory.create_batch(30, romancista_id=romancista.id)
    )

    response = client.get('/livros/query/')

    limite_por_pagina = 20
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == limite_por_pagina


def test_busca_livro_por_query_vazias_retorna_lista_total(
    client, session, romancista
):
    # factory
    session.bulk_save_objects(
        LivroFactory.create_batch(7, romancista_id=romancista.id)
    )

    response = client.get('/livros/query/')

    numero_total_de_registro = 7
    assert response.status_code == HTTPStatus.OK
    assert len(response.json()['livros']) == numero_total_de_registro


def test_busca_livro_por_query_sem_correspondencia_titulo_retorna_lista_vazia(
    client, livro, outro_livro
):
    titulo_sem_correspondecia = 'semcorrespondencia'
    response = client.get(f'/livros/query/?titulo={titulo_sem_correspondecia}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'livros': []}


def test_busca_livro_por_query_sem_correspondencia_ano_retorna_lista_vazia(
    client, livro, outro_livro
):
    ano_sem_correspondencia = 2024
    response = client.get(f'/livros/query/?ano={ano_sem_correspondencia}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'livros': []}


def test_busca_livros_por_romancista_id_ok_e_quantidade_certa(
    session, client, romancista, livro, outro_livro
):
    session.bulk_save_objects(
        LivroFactory.create_batch(4, romancista_id=romancista.id)
    )
    response = client.get(f'/livros/romancista/{romancista.id}')

    assert response.status_code == HTTPStatus.OK

    check_db = session.scalars(
        select(Livro).where(Livro.romancista_id == romancista.id)
    )
    assert len(check_db.fetchall()) == len(response.json()['livros'])


# test lista igual
def test_busca_livros_por_romancista_id_ok_e_lista_certa(
    client, romancista, livro, outro_livro
):
    response = client.get(f'/livros/romancista/{romancista.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'livros': [
            {
                'id': livro.id,
                'titulo': livro.titulo,
                'ano': livro.ano,
                'romancista_id': livro.romancista_id,
            }
        ]
    }


# test falha sem livro por romancista
def test_busca_livros_por_romancista_id_sem_livros_retorna_lista_vazia(
    client, romancista
):
    response = client.get(f'/livros/romancista/{romancista.id}')

    assert response.json() == {'livros': []}
    assert response.status_code == HTTPStatus.OK


# test falha por romancista id
def test_busca_livros_por_romancista_id_retorna_erro_nao_cadastrado(client):
    romancista_id = 1
    response = client.get(f'/livros/romancista/{romancista_id}')

    assert response.json() == {'detail': 'Romancista não consta no MADR'}
    assert response.status_code == HTTPStatus.NOT_FOUND
