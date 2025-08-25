'''
**This shouldn't be used in prod**
    Extracts levels from scp and uploads them to the server. Each upload is made with a new fictional user

How to use:
    pip install tqdm

    Unzip your scp and move it to project root
    Name it "unzipped_scp"
    Run this from project root
'''

UNZIP_SOURCE = 'unzipped_scp/sonolus' # make sure .gitignore covers it

from asyncio import run
from os import listdir
from env import env
from sonolus_server.models import *
import json
from tqdm import tqdm
import random
import string

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from contextlib import asynccontextmanager
from typing import AsyncGenerator

import aiobotocore.session as aiobotocore

async def main():
    engine = create_async_engine(env.DATABASE_LINK, echo=env.IS_DEV)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            yield session

    data: list[tuple[User, Level]] = []

    for filename in listdir(UNZIP_SOURCE + '/levels'):
        try:
            with open(f'{UNZIP_SOURCE}/levels/{filename}', 'r', encoding='utf-8') as file:
                json_content = json.load(file)

                user = User(
                    id=''.join(random.choices(string.ascii_letters + string.digits, k=64)),
                    name=json_content['item']['author'],
                    handle='010101'
                )

                level = Level(
                    title=json_content['item']['title'],
                    producer=json_content['item']['artists'],
                    artist=None,
                    difficulty=json_content['item']['rating'],
                    description=json_content['description'],
                    visibility=Visibility.PUBLIC,
                    id=''.join(random.choices(string.ascii_letters + string.digits, k=20)),
                    user_id=user.id,
                    is_anonymous=False,
                    user_name=user.name,
                    user_handle='010101',
                    data_hash=json_content['item']['data']['hash'],
                    bgm_hash=json_content['item']['bgm']['hash'],
                    cover_hash=json_content['item']['cover']['hash'],
                    preview_hash=json_content['item']['preview']['hash'],
                    timestamp=0
                )

                level.set_meta()

                data.append([user, level])
        except KeyError:
            print(f'keyerror in {filename} - skipping')

    async with get_session() as session:
        async with aiobotocore.get_session().create_client(
            's3',
            endpoint_url=env.S3_API_ENDPOINT,
            aws_access_key_id=env.S3_ACCESS_KEY,
            aws_secret_access_key=env.S3_SECRET_KEY,
        ) as s3:
            for user, level in tqdm(data):
                for hash in (level.data_hash, level.bgm_hash, level.preview_hash, level.cover_hash):
                    with open(f'{UNZIP_SOURCE}/repository/{hash}', 'rb') as file:
                        data = file.read()

                    await s3.put_object(
                        Bucket=env.S3_BUCKET_NAME,
                        Key=hash,
                        Body=data
                    )
                
                session.add(user)
                session.add(level)
                await session.commit()

run(main())