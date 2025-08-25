from fastapi import APIRouter, Depends
from ..types import localization
from ..models import *
from ..strings import get_language
from .. import static
from ..dependencies import GetUser
from .. import database
from env import env

router = APIRouter()

@router.get('/info', response_model=ServerInfo)
async def main(localization: localization='en'):
    language = get_language(localization)

    return ServerInfo(
        title='2tls',
        description=language['description'],
        buttons=[
            ServerInfoButton(type='authentication'),
            ServerInfoButton(type='post'),
            ServerInfoButton(type='level'),
            ServerInfoButton(type='skin'),
            ServerInfoButton(type='background'),
            ServerInfoButton(type='effect'),
            ServerInfoButton(type='particle'),
            ServerInfoButton(type='engine'),
            ServerInfoButton(type='configuration')
        ],
        configuration=ServerConfiguration(
            options=[
                ServerTextOption(
                    query='always_set_alias',
                    name=language['always_set_alias_name'],
                    description=language['always_set_alias_description'],
                    required=False,
                    **{'def': ''},
                    placeholder='#NAME_PLACEHOLDER',
                    limit=64,
                    shortcuts=[]
                ),
                ServerToggleOption(
                    query='always_hide_id',
                    name=language['always_hide_id_name'],
                    description=language['always_hide_id_description'],
                    required=False,
                    **{'def': False}
                )
            ]
        )
    )

@router.get('/levels/info', response_model=ServerItemInfo)
async def levels(always_set_alias: str | None = None, always_hide_id: Literal['0', '1'] = '0', localization: localization='en', user: User = Depends(GetUser())):
    language = get_language(localization)

    sections=[ServerItemSection(
        title='#NEWEST',
        icon='arrowDown',
        itemType='level',
        items=await database.level_cache.get_page(page_size=5) 
    )]

    if user:
        sections.insert(0, ServerItemSection(
            title=language['my_levels'],
            icon='post',
            itemType='level',
            items=[
                LevelItem(
                    name=f'{env.PROJECT_NAME}-my-levels',
                    rating=0,
                    title=language['my_levels'],
                    artists='',
                    author='',
                    tags=[],
                    engine=static.engine,
                    useSkin=UseItem(useDefault=True),
                    useBackground=UseItem(useDefault=True),
                    useEffect=UseItem(useDefault=True),
                    useParticle=UseItem(useDefault=True),
                    cover=Srl(url=''),
                    bgm=Srl(url=''),
                    data=Srl(url='')
                )
            ]
        ))

    return ServerItemInfo(
        creates=[
            ServerForm(
                type='',
                title='#UPLOAD',
                icon='arrowUp',
                description='\n\n', # f'{language['create_level_description']}\n\n',
                requireConfirmation=True,
                options=[
                    ServerTextOption(
                        query='title',
                        name='#TITLE',
                        required=True,
                        **{'def': ''},
                        placeholder='#TITLE_PLACEHOLDER',
                        limit=128,
                        shortcuts=[]
                    ),
                    ServerTextOption(
                        query='producer',
                        name=language['producer'],
                        required=True,
                        **{'def': ''},
                        placeholder=language['producer_placeholder'],
                        limit=64,
                        shortcuts=[]
                    ),
                    ServerTextOption(
                        query='artist',
                        name='#ARTISTS',
                        required=False,
                        **{'def': ''},
                        placeholder='#ARTISTS_PLACEHOLDER',
                        limit=128,
                        shortcuts=[]
                    ),
                    ServerSliderOption(
                        query='difficulty',
                        name='#DIFFICULTY',
                        required=True,
                        **{'def': 0},
                        min=0,
                        max=99,
                        step=1
                    ),
                    ServerTextAreaOption(
                        query='description',
                        name='#DESCRIPTION',
                        required=False,
                        **{'def': ''},
                        placeholder='#DESCRIPTION_PLACEHOLDER',
                        limit=512,
                        shortcuts=[
                            'BPM: ', 'Length: ', 'Genre: ', 'Source: '
                        ]
                    ),
                    ServerFileOption(
                        query='level_file_upload',
                        name='#LEVEL',
                        description=language['usc_file'],
                        required=True,
                        **{'def': ''}
                    ),
                    ServerFileOption(
                        query='bgm_file_upload',
                        name='#LEVEL_BGM',
                        description=language['bgm_file'],
                        required=True,
                        **{'def': ''}
                    ),
                    ServerFileOption(
                        query='cover_file_upload',
                        name='#LEVEL_COVER',
                        description=f'{language['img_file']}\n{language['better_square']}',
                        required=True,
                        **{'def': ''}
                    ),
                    ServerSelectOption(
                        query='visibility',
                        name=language['visibility'],
                        required=False,
                        **{'def': 'unlisted'},
                        values=[
                            SelectValue(
                                name='public',
                                title=language['visibility_public']
                            ),
                            SelectValue(
                                name='unlisted',
                                title=language['visibility_unlisted']
                            )
                        ]
                    ),
                    ServerTextOption(
                        query='set_alias',
                        name=language['alias_name'],
                        description=language['alias_description'],
                        required=False,
                        **{'def': always_set_alias if always_set_alias else ''},
                        placeholder='#NAME_PLACEHOLDER',
                        limit=64,
                        shortcuts=[]
                    ),
                    ServerToggleOption(
                        query='hide_id',
                        name=language['hide_id_name'],
                        description=language['hide_id_description'],
                        required=False,
                        **{'def': bool(int(always_hide_id))}
                    )
                ]
            )
        ] if user and not user.uploading_restriction_reason else None,
        searches=[
            ServerForm(
                type='advanced',
                title='#ADVANCED',
                icon='advanced',
                requireConfirmation=False,
                options=[
                    ServerTextOption(
                        query='keywords',
                        name='#KEYWORDS',
                        required=False,
                        **{'def': ''},
                        placeholder='#KEYWORDS_PLACEHOLDER',
                        limit=0,
                        shortcuts=[]
                    ),
                    ServerTextOption(
                        query='handle',
                        name=language['search_by_user_handle'],
                        required=False,
                        **{'def': ''},
                        placeholder='000000',
                        limit=0,
                        shortcuts=[]
                    ),
                    ServerSliderOption(
                        query='min_rating',
                        name='#RATING_MINIMUM',
                        required=False,
                        **{'def': 1},
                        min=1,
                        max=99,
                        step=1
                    ),
                    ServerSliderOption(
                        query='max_rating',
                        name='#RATING_MAXIMUM',
                        required=False,
                        **{'def': 99},
                        min=1,
                        max=99,
                        step=1
                    ),
                    ServerSelectOption(
                        query='sort_by',
                        name='#SORT',
                        required=False,
                        **{'def': 'newest'},
                        values=[
                            SelectValue(
                                name='newest',
                                title='#NEWEST'
                            ),
                            SelectValue(
                                name='oldest',
                                title='#OLDEST'
                            ),
                            SelectValue(
                                name='most_liked',
                                title=language['sort_by_most_liked']
                            )
                        ]
                    )
                ]
            )
        ],
        sections=sections
    )

@router.get('/skins/info', response_model=ServerItemInfo)
async def skins(localization: localization='en'):
    return ServerItemInfo(
        sections=[
            ServerItemSection(
                title='#SKIN',
                icon='skin',
                itemType='skin',
                items=[
                    static.skin_old,
                    static.skin_new
                ]
            )
        ]
    )

@router.get('/backgrounds/info', response_model=ServerItemInfo)
async def skins(localization: localization='en'):
    return ServerItemInfo(
        sections=[
            ServerItemSection(
                title='#BACKGROUND',
                icon='background',
                itemType='background',
                items=[static.background]
            )
        ]
    )

@router.get('/effects/info', response_model=ServerItemInfo)
async def effects(localization: localization='en'):
    return ServerItemInfo(
        sections=[
            ServerItemSection(
                title='#EFFECT',
                icon='effect',
                itemType='effect',
                items=[static.effect]
            )
        ]
    )

@router.get('/particles/info', response_model=ServerItemInfo)
async def particles(localization: localization='en'):
    return ServerItemInfo(
        sections=[
            ServerItemSection(
                title='#PARTICLE',
                icon='particle',
                itemType='particle',
                items=[static.particle]
            )
        ]
    )

@router.get('/engines/info', response_model=ServerItemInfo)
async def engines(localization: localization='en'):
    return ServerItemInfo(
        sections=[
            ServerItemSection(
                title='#ENGINE',
                icon='engine',
                itemType='engine',
                items=[static.engine]
            )
        ]
    )