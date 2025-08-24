from fastapi import APIRouter
from ..models import *
from ..types import localization
from .. import static

router = APIRouter()

@router.get('/skins/list', response_model=ServerItemList[SkinItem])
async def skins(localization: localization='en'):
    return ServerItemList(
        pageCount=1,
        items=[
            static.skin_old,
            static.skin_new
        ]
    )

@router.get(f'/skins/{static.skin_old.name}', response_model=ServerItemDetails[SkinItem])
async def skin_old(localization: localization='en'):
    return ServerItemDetails(
        item=static.skin_old,
        actions=[],
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )

@router.get(f'/skins/{static.skin_new.name}', response_model=ServerItemDetails[SkinItem])
async def skin_new(localization: localization='en'):
    return ServerItemDetails(
        item=static.skin_new,
        actions=[],
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )

@router.get('/backgrounds/list', response_model=ServerItemList[BackgroundItem])
async def backgrounds(localization: localization='en'):
    return ServerItemList(
        pageCount=1,
        items=[static.background]
    )

@router.get(f'/backgrounds/{static.background.name}', response_model=ServerItemDetails[BackgroundItem])
async def background(localization: localization='en'):
    return ServerItemDetails(
        item=static.background,
        actions=[],
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )

@router.get('/effects/list', response_model=ServerItemList[EffectItem])
async def effects(localization: localization='en'):
    return ServerItemList(
        pageCount=1,
        items=[static.effect]
    )

@router.get(f'/effects/{static.effect.name}', response_model=ServerItemDetails[EffectItem])
async def effect(localization: localization='en'):
    return ServerItemDetails(
        item=static.effect,
        actions=[],
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )

@router.get('/particles/list', response_model=ServerItemList[ParticleItem])
async def particles(localization: localization='en'):
    return ServerItemList(
        pageCount=1,
        items=[static.particle]
    )

@router.get(f'/particles/{static.particle.name}', response_model=ServerItemDetails[ParticleItem])
async def particle(localization: localization='en'):
    return ServerItemDetails(
        item=static.particle,
        actions=[],
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )

@router.get('/engines/list', response_model=ServerItemList[EngineItem])
async def engines(localization: localization='en'):
    return ServerItemList(
        pageCount=1,
        items=[static.engine]
    )

@router.get(f'/engines/{static.engine.name}', response_model=ServerItemDetails[EngineItem])
async def engine(localization: localization='en'):
    return ServerItemDetails(
        item=static.engine,
        actions=[],
        hasCommunity=False,
        leaderboards=[],
        sections=[]
    )