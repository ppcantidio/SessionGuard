from app.exceptions import SessionExpired
from app.models.auth_models import SanitazedSession
from app.services.session_service import SessionService
from app.services.token_service import TokenService


class CheckAuth:
    def __init__(
        self, session_service: SessionService, token_service: TokenService
    ) -> None:
        self.session_service = session_service
        self.token_service = token_service

    async def execute(self, token: str) -> SanitazedSession:
        token_data = await self.token_service.decode_token(token)

        session_id = token_data.session_id
        user_id = token_data.user.user_id

        session = await self.session_service.get_session(session_id, user_id)
        if session is None:
            raise SessionExpired()

        sanitazed_session = session.sanitaze()
        return sanitazed_session
