from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict

from app.models.user import User

json_encoders = {datetime: lambda v: int(v.timestamp()), UUID4: lambda v: str(v)}


class Token(BaseModel):
    model_config = ConfigDict(json_encoders=json_encoders, strict=False)

    token: str
    expires_at: Optional[datetime] = None


class ProviderTokens(BaseModel):
    access_token: Token
    refresh_token: Optional[Token] = None


class SanitazedSession(BaseModel):
    model_config = ConfigDict(strict=False)

    session_id: str
    user: User
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
    user: User
    exp: datetime
    iat: datetime
