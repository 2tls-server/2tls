from fastapi import Header, HTTPException
from . import database
from .models import User
# from sqlmodel import select

from env import env

class GetUser:
    def __init__(self, return_session: bool = False, raise_exc: bool = False, return_user: bool = True):
        self.return_session = return_session
        self.raise_exc = raise_exc
        self.return_user = return_user

    async def __validate_session(self, session: str | None) -> str | None:
        async with database.redis_client.client() as redis:
            if not session or not (user_id := await redis.get(f'{env.PROJECT_NAME}:session:{session}')):
                return None
        
        return user_id

    async def __get_user(self, user_id: str) -> User | None:
        async with database.redis_client.client() as redis:
            json = await redis.get(f'{env.PROJECT_NAME}:user:{user_id}')

        if not json:
            return None

        return User.model_validate_json(json)

    async def __call__(self, session: str | None = Header(None, alias='Sonolus-Session')) -> User | None | tuple[User | None, str | None] | str:
        user_id = await self.__validate_session(session)

        if not user_id:
            if self.raise_exc:
                raise HTTPException(401)
            if self.return_session and self.return_user:
                return None, None
            return None

        user = await self.__get_user(user_id)

        if not user:
            if self.raise_exc:
                raise HTTPException(401)
            if self.return_session and self.return_user:
                return None, None
            return None

        if self.return_session:
            if self.return_user:
                return user, session
            return session
        return user