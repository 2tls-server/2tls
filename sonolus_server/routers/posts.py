from fastapi import APIRouter, HTTPException
from ..types import localization
from ..models import *
from env import env
from ..strings import get_language

router = APIRouter()

@router.get('/posts/info', response_model=ServerItemInfo)
async def posts(localization: localization='en'):
    language = get_language(localization)

    return ServerItemInfo(
        sections=[
            ServerItemSection(
                title='#ALL',
                icon='award',
                itemType='post',
                items=[
                    PostItem(
                        name=f'{env.PROJECT_NAME}-guidelines',
                        title=language['guidelines_title'],
                        time=0,
                        author='2tls',
                        tags=[]
                    )
                ]
            )
        ]
    )

@router.get(f'/posts/{env.PROJECT_NAME}-{{post_name}}', response_model=ServerItemDetails[PostItem])
async def post(post_name: str, localization: localization='en'):
    language = get_language(localization)

    title: str
    description: str

    match post_name:
        case 'guidelines':
            title = language['guidelines_title']
            description = language['guidelines']
        case _:
            raise HTTPException(404)
        
    return ServerItemDetails(
        item=PostItem(
            name=f'{env.PROJECT_NAME}-{post_name}',
            title=title,
            time=0,
            author='2tls',
            tags=[]
        ),
        description=description,
        actions=[],
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )