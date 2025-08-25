from fastapi import APIRouter

router = APIRouter(prefix='/api')

__all__ = ['router']

@router.get('/')
async def root():
    return 'The website is WIP. Come back later. You can join the discord server tho!! https://discord.gg/fa5nJEsXH7'