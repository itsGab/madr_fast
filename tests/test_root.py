from http import HTTPStatus

from fastapi.testclient import TestClient

from madr_fast.app import app


def test_root_returns_message():
    client = TestClient(app)

    response = client.get('/')

    assert response.json() == {'message': 'Bem-vindo!'}
    assert response.status_code == HTTPStatus.OK
