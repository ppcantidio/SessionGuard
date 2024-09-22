from abc import ABC
from typing import Optional

from pydantic import BaseModel

from app.models.auth_models import ProviderTokens


class OAuth2User(BaseModel):
    id: str
    email: Optional[str]


class OAuth2Interface(ABC):
    async def get_token(self, code: str) -> ProviderTokens:
        pass

    async def get_user(self, token: str) -> OAuth2User:
        pass
