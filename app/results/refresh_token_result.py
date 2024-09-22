from pydantic import BaseModel

from app.models.auth_models import SanitazedSession, Token


class RefreshTokenResult(BaseModel):
    session: SanitazedSession
    access_token: Token
