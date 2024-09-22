from typing import Optional

import bcrypt

from app.models.auth_models import ProviderTokens
from app.models.user import User
from app.results.auth_result import AuthResult
from app.services.session_service import SessionService
from app.services.token_service import TokenService


class AuthService:
    def __init__(
        self, session_service: SessionService, token_service: TokenService
    ) -> None:
        self.session_service = session_service
        self.token_service = token_service

    async def auth(
        self, user: User, provider_tokens: Optional[ProviderTokens] = None
    ) -> AuthResult:
        session = await self.session_service.create_session(user, provider_tokens)
        token = await self.token_service.create_token(session=session)
        sanitazed_session = session.sanitaze()
        auth_result = AuthResult(
            session=sanitazed_session,
            access_token=token,
            refresh_token=session.refresh_token,
        )
        return auth_result

    async def encrypt_password(self, password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")

    async def check_password(self, user: User, password: str) -> bool:
        if user.hashed_password is None:
            return False
        return bcrypt.checkpw(
            password.encode("utf-8"), user.hashed_password.encode("utf-8")
        )
