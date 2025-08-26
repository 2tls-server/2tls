from fastapi import FastAPI, Request, status, responses
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, select, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
import sonolus_server
import website_api

from env import env

from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

if env.IS_DEV:
    from fakeredis import FakeAsyncRedis as Redis
else:
    from redis.asyncio import Redis

import sonolus_server.database as database

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = create_async_engine(env.DATABASE_LINK, echo=env.IS_DEV)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    database.redis_client = Redis.from_url(env.REDIS_LINK, decode_responses=True)
    database.session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    database.level_cache = database.LevelCache()

    async with database.get_session() as session:
        await database.redis_client.set(
            f'{env.PROJECT_NAME}:level_counter', 
            (await session.execute(select(func.count()).select_from(sonolus_server.models.Level).where(sonolus_server.models.Level.visibility == sonolus_server.models.Visibility.PUBLIC))).scalar_one()
        )

    yield

    await database.redis_client.close()
    
app = FastAPI(
    debug=env.IS_DEV,
    lifespan=lifespan
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f'{exc}'.replace('\n', ' ').replace('   ', ' ')
    # print(exc_str)
    content = {'status_code': 10422, 'message': (await request.body()).decode(), 'data': None}
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

app.include_router(sonolus_server.router)
app.include_router(website_api.router)

@app.get("/")
async def root():
    return responses.RedirectResponse(f'https://open.sonolus.com/2tls.fun')
    # return 'The website is WIP. Come back later. You can join the discord server tho!! https://discord.gg/fa5nJEsXH7'