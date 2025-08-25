from __future__ import annotations

from pydantic import BaseModel, Field, field_validator, ValidationInfo, model_validator
from sqlmodel import SQLModel, Field as SQLField, Relationship
from .types import ServerInfoButton_type, number, ItemType, Text, Icon
from typing import Literal
from enum import Enum
from .misc import int2base, romanize

class ServerInfoButton(BaseModel):
    type: ServerInfoButton_type

class ServerTextOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['text'] = 'text'
    def_: str = Field(..., alias='def')
    placeholder: Text | str
    limit: number
    shortcuts: list[str]

class ServerTextAreaOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['textArea'] = 'textArea'
    def_: str = Field(..., alias='def')
    placeholder: Text | str
    limit: number
    shortcuts: list[str]

class ServerSliderOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['slider'] = 'slider'
    def_: number = Field(..., alias='def')
    min: number
    max: number
    step: number
    unit: Text | str | None = None

class ServerToggleOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['toggle'] = 'toggle'
    def_: bool = Field(..., alias='def')

class SelectValue(BaseModel):
    name: str
    title: Text | str

class ServerSelectOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['select'] = 'select'
    def_: str = Field(..., alias='def')
    values: list[SelectValue]   

class ServerMultiOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['multi'] = 'multi'
    def_: list[bool] = Field(..., alias='def')
    values: list[SelectValue]

class Sil(BaseModel):
    address: str
    name: str

class ServerServerItemOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['serverItem'] = 'serverItem'
    itemType: ItemType
    def_: Sil | None = Field(None, alias='def')
    allowOtherServers: bool

class ServerServerItemsOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['serverItems'] = 'serverItems'
    itemType: ItemType
    def_: list[Sil] = Field(..., alias='def')
    allowOtherServers: bool
    limit: number

class ServerCollectionItemOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['collectionItem'] = 'collectionItem'
    itemType: ItemType

class ServerFileOption(BaseModel):
    query: str
    name: Text | str
    description: str | None = None
    required: bool
    type: Literal['file'] = 'file'
    def_: str = Field(..., alias='def')

type ServerOption = ServerTextOption \
    | ServerTextAreaOption \
    | ServerSliderOption \
    | ServerToggleOption \
    | ServerSelectOption \
    | ServerMultiOption \
    | ServerServerItemOption \
    | ServerServerItemsOption \
    | ServerCollectionItemOption \
    | ServerFileOption 

class ServerConfiguration(BaseModel):
    options: list[ServerOption]

class Srl(BaseModel):
    hash: str | None = None
    url: str | None = None

class ServerInfo(BaseModel):
    title: str
    description: str | None
    buttons: list[ServerInfoButton]
    configuration: ServerConfiguration
    banner: Srl | None = None

class ServerForm(BaseModel):
    type: str
    title: Text | str
    icon: Icon | str | None = None
    description: str | None = None
    help: str | None = None
    requireConfirmation: bool
    options: list[ServerOption]

class Tag(BaseModel):
    title: Text | str
    icon: Icon | str | None = None

class UseItem[T](BaseModel):
    useDefault: bool
    value: T | None = None

    @field_validator('value')
    def validate_value(cls, v: T | None, values) -> T | None:
        useDefault = values.data.get('useDefault')

        if useDefault and v is not None:
            raise ValueError('value must be None when useDefault=True')
        
        if not useDefault and v is None:
            raise ValueError('value is required when useDefault=False')
        
        return v

class PostItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[1] = 1
    title: str
    time: number
    author: str
    tags: list[Tag]
    thumbnail: Srl | None = None

class SkinItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[4] = 4
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    texture: Srl

class BackgroundItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[2] = 2
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    image: Srl
    configuration: Srl

class EffectItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[5] = 5
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    audio: Srl

class ParticleItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[3] = 3
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    thumbnail: Srl
    data: Srl
    texture: Srl

class EngineItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[13] = 13
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    skin: SkinItem
    background: BackgroundItem
    effect: EffectItem
    particle: ParticleItem
    thumbnail: Srl
    playData: Srl
    watchData: Srl
    previewData: Srl
    tutorialData: Srl
    rom: Srl | None = None
    configuration: Srl

class LevelItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[1] = 1
    rating: number
    title: str
    artists: str
    author: str
    tags: list[Tag]
    engine: EngineItem
    useSkin: UseItem[SkinItem]
    useBackground: UseItem[BackgroundItem]
    useEffect: UseItem[EffectItem]
    useParticle: UseItem[ParticleItem]
    cover: Srl
    bgm: Srl
    preview: Srl | None = None
    data: Srl

class PlaylistItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[1] = 1
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    levels: list[LevelItem]
    thumbnail: Srl | None = None

class RoomItem(BaseModel):
    name: str
    title: str
    subtitle: str
    master: str
    tags: list[Tag]
    cover: Srl | None = None
    bgm: Srl | None = None
    preview: Srl | None = None

class ReplayItem(BaseModel):
    name: str
    source: str | None = None
    version: Literal[1] = 1
    title: str
    subtitle: str
    author: str
    tags: list[Tag]
    level: LevelItem
    data: Srl
    configuration: Srl

class ServerItemSection[TItem: (
    PostItem, PlaylistItem, LevelItem,
    SkinItem, BackgroundItem, EffectItem, 
    ParticleItem, EngineItem, ReplayItem,
    RoomItem
)](BaseModel):
    title: Text | str
    icon: Icon | str | None = None
    description: str | None = None
    help: str | None = None
    itemType: Literal['post', 'playlist', 'level', 'skin', 'background', 'effect', 'particle', 'engine', 'replay', 'room']
    items: list[TItem]
    search: ServerForm | None = None
    searchValues: str | None = None

class ServerItemInfo(BaseModel):
    creates: list[ServerForm] | None = None
    searches: list[ServerForm] | None = None
    sections: list[ServerItemSection]
    banner: Srl | None = None

class ServerItemList[T](BaseModel):
    pageCount: number
    cursor: str | None = None
    items: list[T]
    searches: list[ServerForm] | None = None

class ServerItemLeaderboard(BaseModel):
    name: str
    title: Text | str
    description: str | None = None

class ServerItemDetails[T](BaseModel):
    item: T
    description: str | None = None
    actions: list[ServerForm]
    hasCommunity: bool
    leaderboards: list[ServerItemLeaderboard]
    sections: list[ServerItemSection]

class ServerItemLeaderboardRecord(BaseModel):
    name: str
    rank: Text | str
    player: str
    value: Text | str

class ServerItemLeaderboardDetails(BaseModel):
    topRecords: list[ServerItemLeaderboardRecord]

class User(SQLModel, table=True):
    id: str = SQLField(primary_key=True)
    name: str
    anonymous_user: AnonymousUser = Relationship(back_populates='user', sa_relationship_kwargs={"uselist": False})
    uploading_restriction_reason: str | None = None
    handle: str

class AnonymousUser(SQLModel, table=True): 
    id: int | None = SQLField(default=None, primary_key=True)
    user_id: str = SQLField(foreign_key='user.id')
    user: User = Relationship(back_populates='anonymous_user')

    @property
    def handle(self) -> str:
        return int2base(self.id, 36).zfill(6)

class ServiceUserProfile(BaseModel):
    id: str
    name: str
    handle: str
    avatarType: str
    avatarForegroundType: str
    avatarForegroundColor: str
    avatarBackgroundType: str
    avatarBackgroundColor: str
    bannerType: str
    aboutMe: str
    favorites: list[str]


class ServerAuthenticateRequest(BaseModel):
    type: Literal['authenticateServer']
    address: str
    time: number
    userProfile: ServiceUserProfile

class Visibility(str, Enum):
    PUBLIC = 'public'
    UNLISTED = 'unlisted'

class BaseLevel(SQLModel):
    title: str = SQLField(..., max_length=128)
    producer: str = SQLField(..., max_length=64)
    artist: str | None = SQLField(None, max_length=128)
    difficulty: int = SQLField(..., ge=1, le=99)
    description: str = SQLField('', max_length=512)
    visibility: Visibility = Visibility.UNLISTED

class PublicLevel(BaseLevel):
    level_file_upload: str
    bgm_file_upload: str
    cover_file_upload: str
    set_alias: str | None = SQLField(None, max_length=64)
    hide_id: bool | None = None

class Level(BaseLevel, table=True):
    meta: str | None = None

    autoincrement_id: int = SQLField(None, primary_key=True)
    id: str
    user_id: str
    is_anonymous: bool
    user_name: str
    user_handle: str
    data_hash: str
    bgm_hash: str
    cover_hash: str
    preview_hash: str
    likes: int = 0
    timestamp: int

    def set_meta(self):         
        self.meta = f'{romanize(self.title)}{romanize(self.producer)}{romanize(self.artist) if self.artist else ''}{romanize(self.description) if self.description else ''}'

class LevelLike(SQLModel, table=True):
    level_id: str = SQLField(primary_key=True)
    user_id: str = SQLField(primary_key=True)

class ServerCreateItemResponse(BaseModel):
    key: str
    hashes: list[str]
    shouldUpdateInfo: bool | None = None
    shouldNavigateToItem: str | None = None

class ServerAuthenticateResponse(BaseModel):
    session: str
    expiration: number

class ServerUploadItemResponse(BaseModel):
    shouldUpdateInfo: bool | None = None
    shouldNavigateToItem: str | None = None
 
class ServerSubmitItemActionResponse(BaseModel):
    key: str
    hashes: list[str]
    shouldUpdateItem: bool | None = None
    shouldRemoveItem: bool | None = None
    shouldNavigateToItem: str | None = None