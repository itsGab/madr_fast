from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token/')
def token(): ...
