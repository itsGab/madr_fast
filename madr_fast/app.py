from http import HTTPStatus

from fastapi import FastAPI

from madr_fast.routers import auth, contas, livros, romancistas
from madr_fast.schemas import Message

app = FastAPI()
app.include_router(contas.router)
app.include_router(livros.router)
app.include_router(romancistas.router)
app.include_router(auth.router)


@app.get('/', response_model=Message, status_code=HTTPStatus.OK)
def root():
    return {'message': 'Bem-vindo!'}
