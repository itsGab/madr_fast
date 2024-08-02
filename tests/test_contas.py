from http import HTTPStatus


def test_cria_conta_dados_validos_retorna_criado(client):
    # data
    json_input = {
        'username': 'usuario_de_teste',
        'email': 'usuario@de.teste',
        'senha': 'segredo',
    }
    json_output = {  # saida esperada
        'username': 'usuario_de_teste',
        'email': 'usuario@de.teste',
        'id': 1,
    }

    response = client.post('/contas', json=json_input)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == json_output


def test_delete(client, usuario):
    response = client.post(
        '/auth/token',
        data={'username': usuario.email, 'password': usuario.senha_pura},
    )
    token = response.json()['access_token']
    assert token

    response = client.delete(
        f'/contas/{usuario.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'message': 'Conta deletada com sucesso'}
    assert response.status_code == HTTPStatus.OK
