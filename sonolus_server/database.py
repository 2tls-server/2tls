from redis.asyncio import Redis, ConnectionPool
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from .models import LevelItem, Level, UseItem, Srl, Visibility, LevelLike, Tag
from env import env
from fastapi import HTTPException
from sqlmodel import select, col, update
from .static import engine
from asyncio import sleep

redis_pool: ConnectionPool
redis_client: Redis
session_maker: sessionmaker

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session

class LevelCache:
    def __init__(self, override_redis_client: Redis | None=None):
        self.redis = override_redis_client if override_redis_client else redis_client
        self.order_cache_rebuild_lock = False

    def level_to_level_item(self, level: Level, tags: list[Tag] | None = None) -> LevelItem:
        return LevelItem(
            name=f'{env.PROJECT_NAME}-level-{level.id}',
            source=env.FINAL_HOST_LINKS[0],
            rating=level.difficulty,
            title=level.title,
            artists=f'{level.producer}{f' / {level.artist}' if level.artist else ''}',
            author=f'{level.user_name}{'@' if level.is_anonymous else '#'}{level.user_handle}',
            tags=tags if tags else [],
            engine=engine,
            useSkin=UseItem(useDefault=True),
            useBackground=UseItem(useDefault=True), # TODO
            useEffect=UseItem(useDefault=True),
            useParticle=UseItem(useDefault=True),
            cover=Srl(
                hash=level.cover_hash,
                url=f'/sonolus/proxy/{level.cover_hash}'
            ),
            bgm=Srl(
                hash=level.bgm_hash,
                url=f'/sonolus/proxy/{level.bgm_hash}'
            ),
            preview=Srl(
                hash=level.preview_hash,
                url=f'/sonolus/proxy/{level.preview_hash}'
            ),
            data=Srl(
                hash=level.data_hash,
                url=f'/sonolus/proxy/{level.data_hash}'
            )
        )

    async def public_level_counter(self):
        async with self.redis.client() as redis:
            return int(await redis.get(f'{env.PROJECT_NAME}:level_counter') or 0)
    
    async def change_level_counter(self, decr: bool=False):
        async with self.redis.client() as redis:
            await ((redis.decr if decr else redis.incr)(f'{env.PROJECT_NAME}:level_counter'))

    async def add(self, level: Level):
        if self.order_cache_rebuild_lock:
            await sleep(1)
            return await self.add(level)

        level_json = level.model_dump_json()
        level_item_json = self.level_to_level_item(level).model_dump_json()

        async with self.redus.client() as redis:
            await redis.setex(f'{env.PROJECT_NAME}:id_level_cache:{level.id}', 86400, level_json)
            await redis.lpush(f'{env.PROJECT_NAME}:order_level_cache', level_item_json)
            await redis.ltrim(f'{env.PROJECT_NAME}:order_level_cache', 0, 79)
            await redis.sadd(f'{env.PROJECT_NAME}:level_likes:{level.id}', 'id_placeholder') # go to __get_likes_from_db_and_pass_to_redis
            await redis.expire(f'{env.PROJECT_NAME}:level_likes:{level.id}', 86400)

        if level.visibility == Visibility.PUBLIC:
            await self.change_level_counter()

    async def get_single_level(self, id: str) -> Level:
        if len(id) != 20:
            raise HTTPException(404)
        
        async with self.redis.client() as redis:
            level = await redis.get(f'{env.PROJECT_NAME}:id_level_cache:{id}')

            if level:
                if int(await redis.ttl(f'{env.PROJECT_NAME}:id_level_cache:{id}')) < 1600:
                    await redis.expire(f'{env.PROJECT_NAME}:id_level_cache:{id}', 1800)

                return Level.model_validate_json(level)
            
            async with get_session() as session:
                level_in_db = (await session.execute(select(Level).where(Level.id == id))).scalar_one_or_none()

                if not level_in_db:
                    raise HTTPException(404)
                
                await redis.setex(f'{env.PROJECT_NAME}:id_level_cache:{level_in_db.id}', 1800, level_in_db.model_dump_json())

                return level_in_db
    
    async def order_cache_rebuild(self):
        async with get_session() as session, self.redis.client() as redis:
            await redis.delete(f'{env.PROJECT_NAME}:order_level_cache')

            await redis.lpush(
                f'{env.PROJECT_NAME}:order_level_cache',
                *reversed(
                    list(
                        map(
                            lambda x: self.level_to_level_item(x).model_dump_json(), 
                            (
                                await session.execute(
                                    select(Level)
                                    .where(Level.visibility == Visibility.PUBLIC)
                                    .order_by(
                                        col(Level.autoincrement_id)
                                        .desc()
                                    ).limit(80)
                                )
                            ).scalars().all()
                        )
                    )
                )
            )


    async def get_page(self, page_size: int=20, page_num: int=0) -> list[LevelItem]:
        async with self.redis.client() as redis:
            length = await redis.llen(f'{env.PROJECT_NAME}:order_level_cache')

            if env.ALLOW_ORDER_CACHE_REBUILD and length < 79 and not self.order_cache_rebuild_lock:
                self.order_cache_rebuild_lock = True
                await self.order_cache_rebuild()
                self.order_cache_rebuild_lock = False

            if length - 1 < page_size * (page_num + 1):
                async with get_session() as session:
                    return map(
                        self.level_to_level_item,
                        (await session.execute(
                            select(Level)
                            .where(Level.visibility == Visibility.PUBLIC)
                            .order_by(col(Level.autoincrement_id).desc())
                            .offset(page_size * page_num)
                            .limit(page_size)
                        )).scalars().all()
                    )
            
            return list(
                map(
                    lambda x: LevelItem.model_validate_json(x),
                    await redis.lrange(f'{env.PROJECT_NAME}:order_level_cache', page_size * page_num, page_size * (page_num + 1) - 1)
                )
            )
    
    async def __get_likes_from_db_and_pass_to_redis(self, id: str) -> list[str] | None:
        async with get_session() as session, self.redis.client() as redis:
            likes_in_db = (await session.execute(select(LevelLike.user_id).where(LevelLike.level_id == id))).scalars().all()
            
            # If the list is uninitialized, redis will return 0 on attempt to get its length
            # so, to avoid mass database pinging for non-liked levels, I decided to add a placeholder
            # That means that if scard(likes) == 1, there are no likes and there won't be an attempt to get them from db 
            await redis.sadd(f'{env.PROJECT_NAME}:level_likes:{id}', 'id_placeholder', *likes_in_db)
            await redis.expire(f'{env.PROJECT_NAME}:level_likes:{id}', 1800)

            return likes_in_db

    async def get_likes(self, id: str, check_my_like: str | None = None) -> tuple[int, bool]:
        async with self.redis.client() as redis:
            likes = await redis.scard(f'{env.PROJECT_NAME}:level_likes:{id}')

            if not likes:
                likes_in_db = await self.__get_likes_from_db_and_pass_to_redis(id)
                return len(likes_in_db), (check_my_like in likes_in_db) if check_my_like else False
            else:
                if int(await redis.ttl(f'{env.PROJECT_NAME}:level_likes:{id}')) < 1600:
                    # I wanted to set something like "if likes < 10 then 1800 else 3600" but level itself will expire after 1800 regardless, so no point in these shenanigans
                    # I __may__ return to this idea because I can also get like count from level when uploading it to cache tho
                    await redis.expire(f'{env.PROJECT_NAME}:level_likes:{id}', 1800)

            return likes - 1, bool(await redis.sismember(f'{env.PROJECT_NAME}:level_likes:{id}', check_my_like)) if check_my_like and likes != 1 else False

    async def like(self, level_id: str, user_id: str) -> tuple[bool, int]:
        async with get_session() as session, self.redis.client() as redis:
            my_like = (await session.execute(select(LevelLike).where(LevelLike.level_id == level_id).where(LevelLike.user_id == user_id))).scalar_one_or_none()

            if my_like:
                like_count = await session.execute(
                    update(Level)
                    .where(Level.id == level_id)
                    .values(likes=Level.id - 1)
                    .returning(Level.likes)
                )
                await session.delete(my_like)
            else:
                like_count = await session.execute(
                    update(Level)
                    .where(Level.id == level_id)
                    .values(likes=Level.id + 1)
                    .returning(Level.likes)
                )
                session.add(LevelLike(
                    level_id=level_id,
                    user_id=user_id
                ))
            await session.commit()
    
            redis_likes = await redis.scard(f'{env.PROJECT_NAME}:level_likes:{level_id}')

            if not redis_likes:
                await self.__get_likes_from_db_and_pass_to_redis(level_id)
            else:
                if my_like:
                    await redis.srem(f'{env.PROJECT_NAME}:level_likes:{level_id}', user_id)
                else:
                    await redis.sadd(f'{env.PROJECT_NAME}:level_likes:{level_id}', user_id)
            
                if int(await redis.ttl(f'{env.PROJECT_NAME}:level_likes:{level_id}')) < 1600:
                    await redis.expire(f'{env.PROJECT_NAME}:level_likes:{level_id}', 1800)

            return not my_like, like_count
    
    async def __delete_level(self, level_id: str, dont_delete_public_level: bool = False):
        # would love to take level: Level as an argument, but uhh

        async with get_session() as session:
            level = (await session.execute(select(Level).where(Level.id == level_id))).scalar_one()

            if dont_delete_public_level and level.visibility == Visibility.PUBLIC:
                raise HTTPException(400)

            await session.delete(level)
            await session.commit()

            return level

    async def delete_level(self, level_id: str):
        level = await self.__delete_level(level_id)

        async with self.redis.client() as redis:
            await redis.delete(f'{env.PROJECT_NAME}:id_level_cache:{level_id}', f'{env.PROJECT_NAME}:level_likes:{level_id}')

            if level.visibility == Visibility.PUBLIC:
                await redis.lrem(f'{env.PROJECT_NAME}:order_level_cache', 0, self.level_to_level_item(level).model_dump_json())

    async def list_level(self, level_id: str):
        level = await self.__delete_level(level_id, dont_delete_public_level=True)
        level_item_json = self.level_to_level_item(level).model_dump_json()

        new_level = Level.model_validate(level.model_dump(exclude={'autoincrement_id'}))
        new_level.visibility = Visibility.PUBLIC
        new_level_json = new_level.model_dump_json()

        async with get_session() as session:
            session.add(new_level)
            await session.commit()

        async with self.redis.client() as redis:
            await redis.setex(f'{env.PROJECT_NAME}:id_level_cache:{level.id}', 86400, new_level_json)
            await redis.lpush(f'{env.PROJECT_NAME}:order_level_cache', level_item_json)
            await redis.ltrim(f'{env.PROJECT_NAME}:order_level_cache', 0, 79)
            await redis.expire(f'{env.PROJECT_NAME}:level_likes:{level.id}', 86400)

level_cache: LevelCache