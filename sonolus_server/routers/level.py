from fastapi import APIRouter, Query, Depends, HTTPException
from ..models import *
from ..types import localization
from .. import database
from env import env
from math import ceil
from typing import Annotated, Literal
from sqlmodel import select, col, func
from ..dependencies import GetUser
from urllib.parse import parse_qs
from aiobotocore.session import get_session

router = APIRouter()

@router.get('/levels/list', response_model=ServerItemList[LevelItem])
async def level_list(
    page: int = 0, 
    keywords: str = '',
    handle: str = '',
    min_rating: Annotated[int | None, Query(ge=1, le=99)] = 1,
    max_rating: Annotated[int | None, Query(ge=1, le=99)] = 99,
    sort_by: Literal['newest', 'oldest', 'most_liked'] = 'newest',
    localization: localization='en'
):
    cannot_pull_from_cache = bool(keywords or handle or min_rating != 1 or max_rating != 99 or sort_by != 'newest')

    if cannot_pull_from_cache:
        stmt = select(Level).where(Level.visibility == Visibility.PUBLIC)

        if keywords:
            keywords = keywords.lower()

            for keyword in keywords.split(' ')[:10]:
                stmt = stmt.where(col(Level.meta).like(f'%{keyword}%'))

        if handle:
            stmt = stmt.where(Level.user_handle == handle)

        if min_rating != 1:
            stmt = stmt.where(Level.difficulty >= min_rating)

        if max_rating != 99:
            stmt = stmt.where(Level.difficulty <= max_rating)

        async with database.get_session() as session:
            count = (await session.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()

            match sort_by:
                case 'newest':
                    stmt = stmt.order_by(col(Level.autoincrement_id).desc())
                case 'oldest':
                    stmt = stmt.order_by(Level.autoincrement_id)
                case 'most_liked':
                    stmt = stmt.order_by(col(Level.likes).desc(), col(Level.autoincrement_id).desc())

            stmt = stmt.offset(page * 20).limit(20)

            levels = map(database.level_cache.level_to_level_item, (await session.execute(stmt)).scalars())

            return ServerItemList(
                pageCount=ceil(count),
                items=levels
            ) 

    return ServerItemList(
        pageCount=ceil(await database.level_cache.public_level_counter() / 20),
        items=await database.level_cache.get_page(page_num=page)
    )

class ServerSubmitItemActionRequestValues(BaseModel):
    type: Literal['like', 'list', 'delete']

class ServerSubmitItemActionRequest(BaseModel):
    values: str

    def parse(self) -> ServerSubmitItemActionRequestValues:
        params = {k: v[0] for k, v in parse_qs(self.values).items()}
        return ServerSubmitItemActionRequestValues(**params)
    
@router.post (f'/levels/{env.PROJECT_NAME}-level-{{level_id}}/submit', response_model=ServerSubmitItemActionResponse)
async def level_action(level_id: str, action: ServerSubmitItemActionRequest, user: User=Depends(GetUser(raise_exc=True)), localization: localization='en'):
    action_type = action.parse().type
    level = await database.level_cache.get_single_level(level_id)

    match action_type:
        case 'like':
            if user.id == level.user_id:
                raise HTTPException(403)
            
            await database.level_cache.like(level_id, user.id)
            return ServerSubmitItemActionResponse(
                key='',
                hashes=[],
                shouldUpdateItem=True
            )
        case 'list':
            if user.id != level.user_id:
                raise HTTPException(403)
            
            await database.level_cache.list_level(level_id)
            return ServerSubmitItemActionResponse(
                key='',
                hashes=[],
                shouldUpdateItem=True
            )
        case 'delete':
            if user.id != level.user_id:
                raise HTTPException(403)
            
            async with get_session().create_client(
                's3',
                endpoint_url=env.S3_API_ENDPOINT,
                aws_access_key_id=env.S3_ACCESS_KEY,
                aws_secret_access_key=env.S3_SECRET_KEY,
            ) as s3:
                for key in [level.bgm_hash, level.data_hash, level.cover_hash, level.preview_hash]:
                    await s3.delete_object(Bucket=env.S3_BUCKET_NAME, Key=key)
            
            await database.level_cache.delete_level(level_id)
            return ServerSubmitItemActionResponse(
                key='',
                hashes=[],
                shouldRemoveItem=True,
                shouldNavigateToItem='info'
            )

@router.get(f'/levels/{env.PROJECT_NAME}-level-{{level_id}}', response_model=ServerItemDetails[LevelItem])
async def level(level_id: str, user: User | None=Depends(GetUser()), localization: localization='en'):
    level = await database.level_cache.get_single_level(level_id)

    likes, is_liked = await database.level_cache.get_likes(level_id, user.id if user and user.id != level.user_id else None)

    actions: list[ServerForm] = []

    if user:
        if level.user_id == user.id:
            actions.append(ServerForm(
                type='delete',
                title='#DELETE',
                icon='delete',
                requireConfirmation=False,
                options=[]
            ))
            if level.visibility == Visibility.UNLISTED:
                actions.append(ServerForm(
                    type='list',
                    title='#PUBLISH',
                    icon='show',
                    requireConfirmation=False,
                    options=[]
                ))
        else:
            actions.append(
                ServerForm(
                    type='like',
                    title='#LIKED' if is_liked else '#LIKE',
                    icon='heart' if is_liked else 'heartHollow',
                    requireConfirmation=False,
                    options=[]
                )
            )

    return ServerItemDetails(
        item=database.level_cache.level_to_level_item(level, tags=[
            Tag(
                title=str(likes),
                icon='heartHollow'
            )
        ]),
        description=level.description,
        actions=actions,
        hasCommunity=False,
        leaderboards=[], # also TODO but I wanna figure out how to move leaderboard to another place maybe? So caching?
        sections=[]
    )