# Projeto MADR 

Esse é a minha versão do projeto final (ou TCC) para o curso [Curso de FastAPI](https://github.com/dunossauro/fastapi-do-zero) ministrado pelo [Dunossauro (Eduardo Mendes)](https://dunossauro.comhttps://dunossauro.com). Onde o objetivo do projeto é criar um gerenciador de livros e relacionar com seus autores, que chamaremos de MADR (Mader), uma sigla para "Meu Acervo Digital de Romances". Tudo isso em um contexto bastante simplificado, usando as funcionalidades aprendidas no curso.

## 


Conforme proposto no projeto foi feito um API para o gerenciamento de um acervo digital de romances, com livros e romancistas, chamado de MADR (Mader).

O construção do projeto foi toda baseada no material base do curso, buscando manter grande parte do código em português para facilitar o entendimento.

Desafios e como foram abordados:
- Sanitização de input de textos de indentificações (como username, titulo e nome)
- Endpoints adicionais
    - get /livros/romancista_id/{romancista_id} : para buscar livros por romancista
- Resposta dos endpoints que retorvam lista de  items, foi utilizado a lib `fastapi_pagination`, limitando os items em 20 por pagina e traduzindo os `alias` dos campos para o português facilitando o entendimento do usuário
- Schemas
    - updates aceitam campos None (vazio)

# :construction: Ainda em desenvolvimento... :construction:

