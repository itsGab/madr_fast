# factory de livro


def test_busca_livro_por_id_retorna_ok_e_schema(): ...
def test_busca_livro_por_id_id_nao_cadastrado_retorna_erro(): ...
def test_busca_livro_por_query_filtra_nome_parcial_retorna_lista(): ...
def test_busca_livro_por_query_filtra_ano_retorna_lista(): ...
def test_busca_livro_por_query_deve_retorna_paginacao_maiores_que_20(): ...
def test_busca_livro_por_query_vazias_retorna_lista_total(): ...
def test_busca_livro_por_query_sem_correspondencia_retorna_lista_vazia(): ...
