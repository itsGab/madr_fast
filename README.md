# Projeto MADR (Mader)

Esta é a minha versão do projeto final (ou TCC) para o curso [Curso de FastAPI](https://fastapidozero.dunossauro.com), ministrado pelo [Eduardo Mendes (Dunossauro)](https://dunossauro.com). O objetivo é criar um gerenciador de livros e relacionar com seus autores, denominado MADR (Mader), que significa "**Meu Acervo Digital de Romances**". 

O projeto é baseado no material do curso e, por opção, parte do código foi mantida em português para facilitar o entendimento. O projeto utiliza a tecnologia `FastAPI`, e por isso o nome do projeto foi escolhido como `madr_fast`.


## Índice

1. [Visão Geral](#visão-geral)
2. [Tecnologias Utilizadas](#tecnologias-utilizadas)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Funcionalidades](#funcionalidades)
5. [Desafios e Soluções](#desafios-e-soluções)
6. [Como Executar](#como-executar)
7. [Contribuição](#contribuição)
8. [Licença](#licença)


## Visão Geral

O MADR é uma API desenvolvida usando FastAPI para o gerenciamento de um acervo digital de romances, permitindo operações de CRUD (criar, ler, atualizar e deletar) para livros e romancistas. Inclui funcionalidades adicionais como a busca de livros por romancista e paginação dos resultados.


## Tecnologias Utilizadas

### Dependências do Projeto

```toml
[tool.poetry.dependencies]
python = "3.12.*"
fastapi = "^0.111.1"
sqlalchemy = "^2.0.31"
pydantic-settings = "^2.4.0"
alembic = "^1.13.2"
pyjwt = "^2.9.0"
pwdlib = {extras = ["argon2"], version = "^0.2.0"}
python-multipart = "^0.0.9"
pydantic = {extras = ["email"], version = "^2.8.2"}
psycopg = {extras = ["binary"], version = "^3.2.1"}
fastapi-pagination = "^0.12.26"
```

### Dependências de Desenvolvimento

```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.3.2"
pytest-cov = "^5.0.0"
taskipy = "^1.13.0"
ruff = "^0.5.5"
httpx = "^0.27.0"
factory-boy = "^3.3.0"
freezegun = "^1.5.1"
toolong = "^1.5.0"
testcontainers = "^4.7.2"
```

### Taskipy

```toml
[tool.taskipy.tasks]
lint = 'ruff check . ; ruff check . --diff'
format = 'ruff check . --fix ; ruff format .'
run = 'fastapi dev madr_fast/app.py'
pre_test = 'task lint'
test = 'pytest --cov=madr_fast -vv'
post_test = 'coverage html'
```


## Estrutura do Projeto

### Diretórios e Arquivos

```bash
.
├── madr_fast
│   ├── routers
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── contas.py
│   │   ├── livros.py
│   │   └── romancistas.py
│   ├── __init__.py
│   ├── app.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── security.py
│   └── settings.py
├── migrations
│   ├── versions
│   │   └── a01291f63545_criando_o_banco_de_dados.py
│   ├── README
│   ├── env.py
│   └── script.py.mako
├── tests
│   ├── test_contas
│   │   ├── test_atualiza_conta.py
│   │   ├── test_deleta_conta.py
│   │   └── test_registra_conta.py
│   ├── test_livros
│   │   ├── test_altera_livro.py
│   │   ├── test_busca_livro.py
│   │   ├── test_cadastra_livro.py
│   │   └── test_deleta_livro.py
│   ├── test_romancistas
│   │   ├── test_altera_romancista.py
│   │   ├── test_busca_romancista.py
│   │   ├── test_cadastra_romancista.py
│   │   └── test_deleta_romancista.py
│   ├── __init__.py
│   ├── conftest.py
│   ├── factories.py
│   ├── test_app.py
│   ├── test_auth.py
│   ├── test_database.py
│   └── test_security.py
├── .env (<- arquivo no .gitignore)
├── Dockerfile
├── README.md
├── alembic.ini
├── compose.yaml
├── entrypoint.sh
├── notas.md
├── poetry.lock
└── pyproject.toml
```

### Descrição dos Diretórios e Arquivos

#### `madr_fast/`

- **`routers/`**: Contém os roteadores da aplicação.
  - `__init__.py`: Inicializa o pacote `routers`.
  - `auth.py`, `contas.py`, `livros.py`, `romancistas.py`: Roteadores para autenticação, contas, livros e romancistas.
- **`__init__.py`**: Inicializa o pacote principal da aplicação.
- **`app.py`**: Configura e inicializa a aplicação FastAPI.
- **`database.py`**: Configura a conexão com o banco de dados.
- **`models.py`**: Define os modelos de dados da aplicação.
- **`schemas.py`**: Define os esquemas de dados (schemas) e paginação para validação de entrada/saída.
- **`security.py`**: Configura segurança e autenticação.
- **`settings.py`**: Configurações da aplicação.

#### `migrations/`

- **`versions/`**: Scripts de versões de migração de banco de dados.
  - `a01291f63545_criando_o_banco_de_dados.py`: Script de migração para a criação do banco de dados.
- **`README`**: Documento explicativo sobre migrações.
- **`env.py`**: Configuração do ambiente de migração.
- **`script.py.mako`**: Template para geração de scripts de migração.

#### `tests/`

- **`test_contas/`, `test_livros/`, `test_romancistas/`**: Diretórios com testes específicos para cada módulo.
  - **Cada diretório** contém testes para operações como criação, leitura, atualização e exclusão.
- **`__init__.py`**: Inicializa o pacote de testes.
- **`conftest.py`**: Define fixtures e configurações comuns para os testes.
- **`factories.py`**: Define factories para criação de dados de teste.
- **`test_app.py`, `test_auth.py`, `test_database.py`, `test_security.py`**: Testes gerais para partes não específicas dos módulos.

#### Arquivos na Raiz do Projeto

- **`.env`**: Armazena variáveis de ambiente sensíveis (não versionado com Git).
- **`Dockerfile`**: Define a imagem Docker para o projeto.
- **`README.md`**: Este arquivo de documentação.
- **`alembic.ini`**: Configuração para o Alembic.
- **`compose.yaml`**: Configurações do Docker Compose.
- **`entrypoint.sh`**: Script de inicialização para o container Docker.
- **`notas.md`**: Notas ou documentação adicional.
- **`poetry.lock`**: Arquivo de bloqueio de dependências gerado pelo Poetry.
- **`pyproject.toml`**: Arquivo de configuração do projeto, incluindo dependências e configurações de build.


## Funcionalidades

### Documentação da API (Simplificada)

### 1. Contas

- **Registra Conta**
  - **Endpoint**: `POST /contas/`
  - **Descrição**: Registra uma nova conta de usuário.
  - **Autenticação**: Desnecessária.

- **Atualiza Conta**
  - **Endpoint**: `PUT /contas/{id_usuario}`
  - **Descrição**: Atualiza os dados de uma conta existente.
  - **Autenticação**: Necessária autenticação com OAuth2.

- **Deleta Conta**
  - **Endpoint**: `DELETE /contas/{id_usuario}`
  - **Descrição**: Remove uma conta de usuário.
  - **Autenticação**: Necessária autenticação com OAuth2.

### 2. Romancistas

- **Cadastra Romancista**
  - **Endpoint**: `POST /romancistas/`
  - **Descrição**: Cadastra um novo romancista.
  - **Autenticação**: Necessária autenticação com OAuth2.

- **Busca Romancistas Por Id**
  - **Endpoint**: `GET /romancistas/{romancista_id}`
  - **Descrição**: Busca um romancista pelo ID.
  - **Autenticação**: Desnecessária.

- **Altera Romancista**
  - **Endpoint**: `PATCH /romancistas/{romancista_id}`
  - **Descrição**: Atualiza informações de um romancista.
  - **Autenticação**: Necessária autenticação com OAuth2.

- **Deleta Romancista**
  - **Endpoint**: `DELETE /romancistas/{romancista_id}`
  - **Descrição**: Remove um romancista.
  - **Autenticação**: Necessária autenticação com OAuth2.

- **Busca Romancistas Por Query**
  - **Endpoint**: `GET /romancistas/query/`
  - **Descrição**: Busca romancistas com base em parâmetros de consulta.
  - **Autenticação**: Desnecessária.

### 3. Livros

- **Cadastra Livro**
  - **Endpoint**: `POST /livros/`
  - **Descrição**: Cadastra um novo livro.
  - **Autenticação**: Necessária autenticação com OAuth2.

- **Busca Livro Por Id**
  - **Endpoint**: `GET /livros/{livro_id}`
  - **Descrição**: Busca um livro pelo ID.
  - **Autenticação**: Desnecessária.

- **Altera Livro**
  - **Endpoint**: `PATCH /livros/{livro_id}`
  - **Descrição**: Atualiza informações de um livro.
  - **Autenticação**: Necessária autenticação com OAuth2.

- **Deleta Livro**
  - **Endpoint**: `DELETE /livros/{livro_id}`
  - **Descrição**: Remove um livro.
  - **Autenticação**: Necessária autenticação com OAuth2.

- **Busca Livros Por Query**
  - **Endpoint**: `GET /livros/query/`
  - **Descrição**: Busca livros com base em parâmetros de consulta.
  - **Autenticação**: Desnecessária.

- **Busca Livros Por Romancista Id** *`extra`*
  - **Endpoint**: `GET /livros/romancista/{romancista_id}`
  - **Descrição**: Busca livros de um romancista específico.
  - **Autenticação**: Desnecessária.

### 4. Autenticação

- **Login Para Token De Acesso**
  - **Endpoint**: `POST /auth/token`
  - **Descrição**: Solicita um token de acesso para autenticação.
  - **Autenticação**: Desnecessária.

- **Atualiza Token De Acesso**
  - **Endpoint**: `POST /auth/refresh_token`
  - **Descrição**: Atualiza um token de acesso existente.
  - **Autenticação**: Necessária autenticação com OAuth2.


## Desafios e Soluções

### 1. Sanitização de Inputs

- **Desafio**: Garantir que os inputs dos usuários, como nomes de usuário, títulos e nomes, sejam sanitizados.
- **Solução**: Implementação de uma função de validação e sanitização utilizando o `field_validator` do Pydantic. A função `valida_e_sanitiza` é responsável por remover caracteres indesejados e assegurar que os textos contenham apenas letras e números, prevenindo possíveis injeções de SQL e XSS (cross-site scripting). 

**Exemplo de função de validação e sanitização**:
```python
import re
from pydantic import field_validator

def valida_e_sanitiza(text):
    if re.search(r'[^\w\s\à-ÿÀ-Ÿ]', text, re.UNICODE):
        raise ValueError('entrada deve conter apenas letras e números')
    return ' '.join(text.lower().split())

# ...

class UsuarioSchema(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr
    senha: str
# garante que as entradas de texto sejam validades e sanitizadas
    _valida_e_sanitiza = field_validator('username')(valida_e_sanitiza)
```

### 2. Páginação de Resultados

- **Desafio**: Gerenciar e apresentar grandes volumes de dados de maneira eficiente.
- **Solução**: Utilização da biblioteca `fastapi-pagination` para implementar a paginação nos endpoints que retornam listas de itens. Configuração de uma página padrão de 20 itens e tradução dos aliases dos campos para o português para melhorar a experiência do usuário.

**Exemplo de definição paginação**
```python
tamanho_pagina = 20  # itens
T = TypeVar('T')

PaginaLivros = CustomizedPage[
    Page[T],
    UseName('PaginaLivros'),
    UseParamsFields(size=tamanho_pagina),
    UseFieldsAliases(
        items='livros',
        page='página',
        size='tamanho',
        pages='páginas',
    ),
]
```
**Exemplo de output paginação**
```json
{
  "livros": [
    {
      "titulo": "primeiro livro",
      "ano": 1999,
      "romancista_id": 1,
      "id": 1
    },
    {
      "titulo": "segundo livro",
      "ano": 1999,
      "romancista_id": 1,
      "id": 2
    }
  ],
  "total": 2,
  "página": 1,
  "tamanho": 20,
  "páginas": 1
}
```

### 3. Aceita Campos Nulos em `PUT` e `PATCH`

- **Desafio**: Permitir a atualização de registros com campos nulos nos métodos `PUT` e `PATCH`.
- **Solução**: Implementação de lógica para atualizar apenas os campos fornecidos, ignorando campos com valores nulos. Isso permite que você atualize parcialmente um recurso sem a necessidade de fornecer todos os campos.

**Exemplo schema update**
```python
class UsuarioUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=1)
    email: EmailStr | None = None
    senha: str | None = None

    _valida_e_sanitiza = field_validator('username')(valida_e_sanitiza)
```

**Exemplo função de patch**
```python 
@router.patch('/{livro_id}')
def altera_livro(..., livro_update: LivroUpdate,...):
    # ...
    # atualiza os dados do livro para campos diferentes de None
    for chave, valor in livro_update.model_dump(exclude_none=True).items():
        setattr(livro_db, chave, valor)
    # ...
    return livro_db
```
**Observação: No caso de romancista, não usamos campos opcionais porque há apenas o nome que pode ser alterado, e este é um campo obrigatório para a atualização.**

### 4. *Desafio Extra*: Busca de Livros por Romancista Específico
- **Observação**: *Este endpoint foi adicionado como um recurso adicional e não estava originalmente requisitado no projeto.*
- **Desafio**: Permitir a busca de livros associados a um romancista específico.
- **Solução**: Implementação de um endpoint adicional que retorna todos os livros de um romancista identificado pelo `romancista_id`.

**Detalhes do Endpoint**:
`GET /livros/romancista/{romancista_id}`: Retorna uma lista paginada de livros de um romancista específico identificado pelo seu ID. O endpoint retorna um número padrão de 20 livros por página.


## Como Executar

### Configuração do Ambiente

1. **Criação do Arquivo `.env`**

   Crie um arquivo `.env` na raiz do projeto e defina as seguintes variáveis de ambiente:
   ```plaintext
   DATABASE_URL="postgresql+psycopg://app_user:app_password@madrfast_database:5432/app_db"
   SECRET_KEY="sua-chave-secreta"
   ALGORITHM="HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

2. **Instalação das Dependências**

   Certifique-se de que o [Poetry](https://python-poetry.org) está instalado. Instale as dependências do projeto executando:
   ```bash
   poetry install
   ```

### Configuração e Execução com Docker

1. **Construir e Iniciar os Contêineres**

   Use o `docker compose` para construir e iniciar todos os contêineres. O comando `docker compose up` também executa as migrações do banco de dados, conforme configurado no `entrypoint.sh`.

   ```bash
   docker compose up --build
   ```

   Esse comando irá:
   - Construir a imagem Docker conforme definida no `Dockerfile`.
   - Inicializar o contêiner com a aplicação FastAPI e o banco de dados.
   - Executar as migrações do banco de dados automaticamente.

2. **Acessar a Aplicação**

   A aplicação estará disponível em `http://localhost:8000` por padrão e a documentação está disponível em `http://localhost:8000/docs`

### Executar Testes

1. **Rodar Testes**

   Para executar os testes e verificar a cobertura de código, use o comando:
   ```bash
   task test
   ```

   Esse comando carrega um contêiner de banco de dados no docker e executa todos os testes definidos e gera um relatório de cobertura.
