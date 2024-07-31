from fastapi import APIRouter

router = APIRouter('/conta', tags=['conta'])


@router.get('/')
def create_account():
    return {'message': 'Nova conta'}