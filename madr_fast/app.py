from fastapi import FastAPI

from madr_fast.routers import auth, contas, livros, romancistas

app = FastAPI()
app.include_router(contas.router)
app.include_router(livros.router)
app.include_router(romancistas.router)
app.include_router(auth.router)


@app.get('/')
def root():
    return {'message': 'Bem-vindo!'}
