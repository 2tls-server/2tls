from fastapi import APIRouter

router = APIRouter(prefix='/api')

__all__ = ['router']

@router.get('/')
async def root():
    return 'The website is WIP. Come back later'