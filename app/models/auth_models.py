from datetime import datetime
from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict

json_encoders = {datetime: lambda v: int(v.timestamp()), UUID4: lambda v: str(v)}


class UserSession(BaseModel):
    user_id: UUID4
    username: str
    provider_name: Optional[str] = None
    user_provider_id: Optional[str] = None
    permissions: List[str]


class Token(BaseModel):
    model_config = ConfigDict(json_encoders=json_encoders, strict=False)

    token: str
    expires_at: datetime


class ProviderTokens(BaseModel):
    access_token: Token
    refresh_token: Token


class SanitazedSession(BaseModel):
    model_config = ConfigDict(strict=False)

    session_id: str
    user: UserSession
    created_at: datetime
    expires_at: datetime


class Session(SanitazedSession):
    provider_tokens: Optional[ProviderTokens] = None
    refresh_token: Token

    def sanitaze(self) -> SanitazedSession:
        return SanitazedSession(
            session_id=self.session_id,
            user=self.user,
            created_at=self.created_at,
            expires_at=self.expires_at,
        )


class TokenData(BaseModel):
    model_config = ConfigDict(json_encoders=json_encoders, strict=False)

    session_id: str
    user: UserSession
    exp: datetime
    iat: datetime
