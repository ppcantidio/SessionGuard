import asyncio
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

import jwt
import redis.asyncio as aioredis

from app.config import app_config
from app.models.session import Session
from app.models.token_data import TokenData


class SessionService:
    def __init__(self, redis_url: str) -> None:
        self.redis = aioredis.from_url(redis_url)

    def session_key(self, user_id: UUID, session_id: UUID) -> str:
        return f"session:{user_id}:{session_id}"

    async def create_token(self, token_data: TokenData) -> str:
        token_dict = token_data.model_dump()
        token_dict["exp"] = int(token_dict["exp"].timestamp())
        token_dict["iat"] = int(token_dict["iat"].timestamp())
        token_dict["session_id"] = str(token_dict["session_id"])
        token_dict["user_id"] = str(token_dict["user_id"])

        encoded_jwt = jwt.encode(
            token_dict, app_config.secret_key, algorithm=app_config.algorithm
        )
        return encoded_jwt

    async def decode_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, app_config.secret_key, algorithms=[app_config.algorithm]
            )
            return TokenData(
                user_id=UUID(payload["user_id"]),
                session_id=UUID(payload["session_id"]),
                roles=payload["roles"],
                exp=datetime.fromtimestamp(payload["exp"]),
                iat=datetime.fromtimestamp(payload["iat"]),
            )
        except jwt.PyJWTError:
            raise Exception("Could not validate credentials")

    async def create_session(
        self, user_id: UUID, roles: List[str], ttl_seconds: int = 3600
    ) -> Session:
        session_id = uuid4()

        iat_datetime = datetime.now()
        exp_datetime = iat_datetime + timedelta(seconds=ttl_seconds)

        token_data = TokenData(
            user_id=user_id,
            session_id=session_id,
            roles=roles,
            exp=exp_datetime,
            iat=iat_datetime,
        )

        key = self.session_key(user_id, session_id)
        token = await self.create_token(token_data)

        await self.redis.set(key, token, ex=ttl_seconds)

        session = Session(**token_data.model_dump(), token=token)
        return session

    async def get_session(self, session_id: UUID, user_id: UUID) -> Optional[Session]:
        key = self.session_key(user_id, session_id)
        token = await self.redis.get(key)

        if token is None:
            return None

        token_data = await self.decode_token(token)

        session = await self._map_session(token_data, token)
        return session

    async def logout(self, session_id: str, user_id: str) -> None:
        key = self.session_key(user_id, session_id)
        await self.redis.delete(key)

    async def get_all_sessions(self, user_id: str) -> List[Session]:
        pattern = f"session:{user_id}:*"
        session_keys = await self.redis.keys(pattern)

        async def fetch_session(key: str) -> Optional[Session]:
            token = await self.redis.get(key)
            if token:
                token_data = await self.decode_token(token)
                session = await self._map_session(token_data, token)
                return session
            return None

        sessions = await asyncio.gather(*[fetch_session(key) for key in session_keys])

        return [session for session in sessions if session is not None]

    async def logout_all(self, user_id: UUID) -> None:
        pattern = f"session:{user_id}:*"
        session_keys = await self.redis.keys(pattern)
        if session_keys:
            await self.redis.delete(*session_keys)

    async def _map_session(self, token_data: TokenData, token: str) -> Session:
        return Session(**token_data.model_dump(), token=token)
