import asyncio
import json
import secrets
from datetime import datetime, timedelta
from typing import List, Optional
from uuid import UUID, uuid4

import redis.asyncio as aioredis

from app.config import app_config
from app.models import User
from app.models.auth_models import ProviderTokens, Session, Token


class SessionService:
    def __init__(self, redis_url: str) -> None:
        self.redis = aioredis.from_url(redis_url)

    def session_key(self, user_id: UUID, session_id: UUID) -> str:
        return f"session:{user_id}:{session_id}"

    async def create_session(
        self,
        user: User,
        provider_tokens: Optional[ProviderTokens] = None,
    ) -> Session:
        session_id = uuid4()

        ttl_seconds = timedelta(days=app_config.session_expirate_days).total_seconds()

        created_at = datetime.now()
        expires_at = created_at + timedelta(seconds=ttl_seconds)

        refresh_token_expires_at = expires_at - timedelta(hours=1)

        refresh_token = Token(
            token=secrets.token_urlsafe(64), expires_at=refresh_token_expires_at
        )

        session = Session(
            session_id=session_id,
            user=user,
            created_at=created_at,
            expires_at=expires_at,
            provider_tokens=provider_tokens,
            refresh_token=refresh_token,
        )

        key = self.session_key(user.user_id, session_id)

        session_json_str = session.model_dump_json()

        await self.redis.set(key, session_json_str, ex=ttl_seconds)

        return session

    async def get_session(self, session_id: UUID, user_id: UUID) -> Optional[Session]:
        key = self.session_key(user_id, session_id)
        session_str = await self.redis.get(key)

        if session_str is None:
            return None

        session = await self._map_session(session_str)
        return session

    async def logout(self, session_id: UUID, user_id: UUID) -> None:
        key = self.session_key(user_id, session_id)
        await self.redis.delete(key)

    async def get_all_sessions(self, user_id: str) -> List[Session]:
        pattern = f"session:{user_id}:*"
        session_keys = await self.redis.keys(pattern)
        session_ids = [session_key.split(":")[-1] for session_key in session_keys]
        sessions = await asyncio.gather(
            *[self.get_session(session_id) for session_id in session_ids]
        )
        return [session for session in sessions if session is not None]

    async def logout_all(self, user_id: UUID) -> None:
        pattern = f"session:{user_id}:*"
        session_keys = await self.redis.keys(pattern)
        if session_keys:
            await self.redis.delete(*session_keys)

    async def _map_session(self, session_str: str) -> Session:
        session_dict = json.loads(session_str)
        session = Session(**session_dict)
        return session
