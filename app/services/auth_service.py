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

    async def auth(self, user: User, provider_tokens: ProviderTokens) -> AuthResult:
        session = await self.session_service.create_session(user, provider_tokens)
        token = await self.token_service.create_token(session=session)
        sanitazed_session = session.sanitaze()
        auth_result = AuthResult(
            session=sanitazed_session,
            access_token=token,
            refresh_token=session.refresh_token,
        )
        return auth_result
