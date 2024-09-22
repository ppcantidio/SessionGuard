from pydantic import BaseModel

from app.models.auth_models import SanitazedSession, Token


class AuthResult(BaseModel):
    session: SanitazedSession
    access_token: Token
    refresh_token: Token
