from sqlalchemy import select

from madr_fast.models import Usuario


def test_database(session):
    novo_usuario = Usuario(
        username='usuario_de_teste',
        email='usuario@de.teste',
        senha='segredo',
    )
    session.add(novo_usuario)
    session.commit()

    usuario_db = session.scalar(
        select(Usuario).where(Usuario.username == 'usuario_de_teste')
    )

    assert usuario_db.username == 'usuario_de_teste'
    assert usuario_db.created_at
