from http import HTTPStatus

from fastapi import APIRouter

from madr_fast.schemas import UsuarioResponse, UsuarioSchema
from madr_fast.settings import Settings

settings = Settings()

router = APIRouter(prefix='/contas', tags=['contas'])


@router.post(
    '/', response_model=UsuarioResponse, status_code=HTTPStatus.CREATED
)
def criar_conta(user: UsuarioSchema):
    return user
