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
    }

    response = client.post('/contas', json=json_input)

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == json_output
