from fastapi import APIRouter

from madr_fast.schemas import LivroResponse, LivroSchema

router = APIRouter(prefix='/livros', tags=['livros'])


@router.post('/', response_model=LivroResponse)
def cadastrar_livro(livro: LivroSchema):
    return livro
