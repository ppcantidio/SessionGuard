from app.services.session_service import SessionService
from app.usecases.check_auth import CheckAuth


class LogoutAll:
    def __init__(self, check_auth: CheckAuth, session_service: SessionService) -> None:
        self.check_auth = check_auth
        self.session_service = session_service

    async def execute(self, token: str) -> None:
        sanitezed_session = await self.check_auth.execute(token)
        await self.session_service.logout_all(sanitezed_session.user.user_id)
