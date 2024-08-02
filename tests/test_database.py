from sqlalchemy import select

from madr_fast.models import Usuario


def test_database(session, usuario):
    usuario_db = session.scalar(
        select(Usuario).where(Usuario.username == usuario.username)
    )

    assert usuario_db.username == usuario.username
    assert usuario_db.created_at
