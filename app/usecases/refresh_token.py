from app.exceptions import InvalidRefreshToken, SessionExpired
from app.results.refresh_token_result import RefreshTokenResult
from app.services.session_service import SessionService
from app.services.token_service import TokenService


class RefreshToken:
    def __init__(self, token_service: TokenService, session_service: SessionService):
        self.token_service = token_service
        self.session_service = session_service

    async def execute(self, refresh_token: str) -> RefreshTokenResult:
        refresh_token_data = await self.token_service.decode_refresh_token(
            refresh_token
        )

        session_id = refresh_token_data.session_id
        user_id = refresh_token_data.user_id

        session = await self.session_service.get_session(session_id, user_id)
        if session is None:
            raise SessionExpired()

        if refresh_token != session.refresh_token.token:
            raise InvalidRefreshToken()

        access_token = await self.token_service.create_token(user_id)

        sanitazed_session = session.sanitaze()

        refresh_token_result = RefreshTokenResult(
            access_token=access_token, session=sanitazed_session
        )
        return refresh_token_result
