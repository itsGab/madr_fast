from http import HTTPStatus

from sqlalchemy import select

from madr_fast.models import Livro, Usuario
from tests.factories import LivroFactory


def test_database(session, usuario):
    usuario_db = session.scalar(
        select(Usuario).where(Usuario.username == usuario.username)
    )

    assert usuario_db.username == usuario.username
    assert usuario_db.created_at


def test_relacionamento_romancista_e_livro_com_delete(
    session, client, token, romancista, outro_romancista
):
    session.bulk_save_objects(  # romancista 1
        LivroFactory.create_batch(4, romancista_id=romancista.id)
    )
    session.bulk_save_objects(  # romancista 2
        LivroFactory.create_batch(2, romancista_id=outro_romancista.id)
    )

    # verifica livros cadastrados por romancista 1
    check_db = session.scalars(
        select(Livro).where(Livro.romancista_id == romancista.id)
    )
    num_livros_do_romancista = 4
    assert len(check_db.fetchall()) == num_livros_do_romancista

    response = client.delete(
        f'/romancistas/{romancista.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Romancista deletado no MADR'}

    # verifica livros do romancista 1 foram deletados junto
    check_db = session.scalars(
        select(Livro).where(Livro.romancista_id == romancista.id)
    )
    assert not check_db.fetchall()

    # verifica livros do romancista 2 continuam cadastrados
    check_db = session.scalars(select(Livro))
    num_livros_devem_restar_no_db = 2
    assert len(check_db.fetchall()) == num_livros_devem_restar_no_db
