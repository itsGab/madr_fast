from http import HTTPStatus

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from madr_fast.routers import auth, contas, livros, romancistas
from madr_fast.schemas import Message

app = FastAPI()
app.include_router(contas.router)
app.include_router(romancistas.router)
app.include_router(livros.router)
app.include_router(auth.router)
add_pagination(app)


@app.get(
    '/',
    response_model=Message,
    status_code=HTTPStatus.OK,
    include_in_schema=False,
)
def read_root():
    return {'message': 'Bem-vindo!'}
