from http import HTTPStatus

from fastapi import APIRouter

from madr_fast.schemas import UsuarioResponse, UsuarioSchema

router = APIRouter(prefix='/contas', tags=['contas'])


@router.post(
    '/', response_model=UsuarioResponse, status_code=HTTPStatus.CREATED
)
def criar_conta(user: UsuarioSchema):
    return user
