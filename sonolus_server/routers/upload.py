from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Header
from ..models import *
from ..types import localization
from urllib.parse import parse_qs
from ..dependencies import GetUser
from .. import database
from env import env
import secrets
from ..misc import get_id
from aiobotocore.session import get_session
from asyncio import to_thread
from PIL import Image
from io import BytesIO
from asyncio import to_thread, gather, create_task
from pydub import AudioSegment
from ..processors.level import process_level
from hashlib import sha1
from traceback import print_exc
from sqlmodel import select
from time import time

router = APIRouter()

class LevelUpload(BaseModel):
    values: str

    def parse(self) -> PublicLevel:
        params = {k: v[0] for k, v in parse_qs(self.values).items()}
        return PublicLevel(**params)
    
class LevelAndUser(BaseModel):
    level: PublicLevel
    user: User

@router.post('/levels/create', response_model=ServerCreateItemResponse)
async def create_level(
    unparsed_level: LevelUpload, 
    user: User = Depends(GetUser(raise_exc=True)), 
    localization: localization='en',
):
    if user.uploading_restriction_reason:
        raise HTTPException(403)

    level = unparsed_level.parse()

    upload_key = secrets.token_urlsafe(32)
    await database.redis_client.setex(f'{env.PROJECT_NAME}:level_upload:{upload_key}', 60 * 60, LevelAndUser(level=level, user=user).model_dump_json())

    return ServerCreateItemResponse(
        key=upload_key, # I didn't understand it, but now it makes sense
                        # so if anyone wonders, why not use session
                        # uhh bc session can expire while uploading
        hashes=[
            level.level_file_upload, level.bgm_file_upload, level.cover_file_upload
        ],
        shouldUpdateInfo=True
    )

async def process_cover(img_bytes: bytes) -> tuple[bytes, str]:
    def process():
        with Image.open(BytesIO(img_bytes)) as img:
            max_side = max(*img.size)
            new_img = Image.new('RGB', (max_side, max_side), (0, 0, 0))
            new_img.paste(img.convert('RGB'), ((max_side - img.width) // 2, (max_side - img.height) // 2))

            new_img = new_img.resize((512, 512), Image.Resampling.LANCZOS)
            buf = BytesIO()

            new_img.save(buf, format='jpeg')
            img_value = buf.getvalue()

            return img_value, sha1(img_value).hexdigest()
    
    try:
        return await to_thread(process)
    except:
        print_exc()
        raise HTTPException(400)

async def process_bgm(bgm_bytes: bytes, preview_offset: int | float = 0) -> tuple[bytes, str, bytes, str]:
    def process():
        audio = AudioSegment.from_file(BytesIO(bgm_bytes))

        bgm_buffer = BytesIO()
        audio.export(bgm_buffer, format='mp3', bitrate='192k')

        preview = audio[int(preview_offset*1000) : int((preview_offset + 20)*1000)]
        preview_buffer = BytesIO()
        preview.export(preview_buffer, format='mp3', bitrate='64k')

        bgm_value = bgm_buffer.getvalue()
        preview_value = preview_buffer.getvalue()

        return bgm_value, sha1(bgm_value).hexdigest(), preview_value, sha1(preview_value).hexdigest()

    try:
        return await to_thread(process)
    except:
        print_exc()
        raise HTTPException(400)
    
async def process_chart(chart_bytes: bytes) -> tuple[bytes, str]:
    def process():
        level_data = process_level(chart_bytes)

        return level_data, sha1(level_data).hexdigest()
    
    try:
        return await to_thread(process)
    except Exception:
        print_exc()
        raise HTTPException(400)

async def get_file(files: list[UploadFile], hash: str) -> bytes:
    for file in files:
        if file.filename == hash:
            return await file.read()
        
    raise HTTPException(401)

@router.post('/levels/upload', response_model=ServerUploadItemResponse)
async def upload_level(
    upload_key: str = Header(alias='Sonolus-Upload-Key'),
    files: list[UploadFile] = File(...), 
    always_set_alias: str | None = None, 
    always_hide_id: Literal['0', '1'] = '0',
    localization: localization='en'
):
    always_hide_id = bool(always_hide_id)

    print('got files')
    if level_json := await database.redis_client.get(f'{env.PROJECT_NAME}:level_upload:{upload_key}'):
        await database.redis_client.delete(f'{env.PROJECT_NAME}:level_upload:{upload_key}')
    else:
        raise HTTPException(403)

    level_and_user = LevelAndUser.model_validate_json(level_json)

    level = level_and_user.level
    user = level_and_user.user

    async with database.get_session() as session:
        user.anonymous_user = (await session.execute(select(AnonymousUser).where(AnonymousUser.user_id == user.id))).scalar_one()

    (cover, cover_hash), (bgm, bgm_hash, preview, preview_hash), (data, data_hash) = await gather(
        process_cover(await get_file(files, level.cover_file_upload)),
        process_bgm(await get_file(files, level.bgm_file_upload), preview_offset=0), # TODO
        process_chart(await get_file(files, level.level_file_upload))
    )

    async with get_session().create_client(
        's3',
        endpoint_url=env.S3_API_ENDPOINT,
        aws_access_key_id=env.S3_ACCESS_KEY,
        aws_secret_access_key=env.S3_SECRET_KEY,
    ) as s3:
        upload_tasks = [create_task(s3.put_object(
            Bucket=env.S3_BUCKET_NAME, Key=key,
            Body=body, ContentType=mime
            )) for body, key, mime in [
                (cover, cover_hash, 'image/jpeg'), (bgm, bgm_hash, 'audio/mpeg'),
                (preview, preview_hash, 'audio/mpeg'), (data, data_hash, 'application/gzip')
        ]]
        await gather(*upload_tasks)

    if level.hide_id is None:
        level.hide_id = always_hide_id

    if level.set_alias is None:
        level.set_alias = always_set_alias

    level_model = Level(
        title=level.title,
        producer=level.producer,
        artist=level.artist,
        difficulty=level.difficulty,
        description=level.description,
        visibility=level.visibility,
        id=get_id(),
        user_id=user.id,
        is_anonymous=level.hide_id,
        user_name=level.set_alias if level.set_alias else user.name,
        user_handle=user.anonymous_user.handle if level.hide_id else user.handle,
        data_hash=data_hash,
        bgm_hash=bgm_hash,
        cover_hash=cover_hash,
        preview_hash=preview_hash,
        timestamp=int(time())
    )
    level_model.set_meta()

    async with database.get_session() as session:
        session.add(level_model)
        await session.commit()
    
    await database.level_cache.add(level_model)

    return ServerUploadItemResponse(
        shouldNavigateToItem=f'{env.PROJECT_NAME}-level-{level_model.id}', 
        shouldUpdateInfo=True
    )