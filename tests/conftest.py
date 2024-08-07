import factory
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from madr_fast.app import app
from madr_fast.database import get_session
from madr_fast.models import Livro, Romancista, Usuario, table_registry
from madr_fast.security import get_password_hash


class UserFactory(factory.Factory):
    class Meta:
        model = Usuario

    username = factory.Sequence(lambda n: f'usuario{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@teste.com')
    senha = factory.LazyAttribute(lambda obj: f'{obj.username}-segredo')


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override
        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@pytest.fixture
def usuario(session):
    segredo = 'segredo'
    usuario = UserFactory(senha=get_password_hash(segredo))
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    usuario.senha_pura = segredo

    return usuario


@pytest.fixture
def outro_usuario(session):
    segredo = 'segredo'
    usuario = UserFactory(senha=get_password_hash(segredo))
    session.add(usuario)
    session.commit()
    session.refresh(usuario)

    usuario.senha_pura = segredo

    return usuario


@pytest.fixture
def token(client, usuario):
    response = client.post(
        '/auth/token',
        data={
            'username': usuario.email,
            'password': usuario.senha_pura,
        },
    )

    return response.json()['access_token']


@pytest.fixture
def romancista(session):
    romancista = Romancista(nome='jorge')

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


@pytest.fixture
def livro(session, romancista):
    livro = Livro(
        titulo='o ultimo romantico', ano=2000, romancista_id=romancista.id
    )

    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro


@pytest.fixture
def outro_romancista(session):
    romancista = Romancista(nome='cleber')

    session.add(romancista)
    session.commit()
    session.refresh(romancista)

    return romancista


@pytest.fixture
def outro_livro(session, outro_romancista):
    livro = Livro(
        titulo='mais romantico mais furioso',
        ano=2005,
        romancista_id=outro_romancista.id,
    )

    session.add(livro)
    session.commit()
    session.refresh(livro)

    return livro
