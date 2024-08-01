from fastapi import APIRouter

from madr_fast.schemas import RomancistaSchema

router = APIRouter(prefix='/romancistas', tags=['romancistas'])


@router.post('/')
def cadastrar_romancista(romancista: RomancistaSchema):
    return romancista
