from app.config import app_config
from app.repositories import user_repository
from app.results.auth_result import AuthResult
from app.services.session_service import SessionService
from app.services.token_service import TokenService


class AuthSession:
    async def execute(self, username: str, password: str):
        session_service = SessionService(redis_url=app_config.redis_url)

        user = await user_repository.get_user_by_username(username)

        if not user:
            raise Exception("User not found")

        is_valid = await user.check_password(password)

        if not is_valid:
            raise Exception("Invalid password")

        session = await session_service.create_session(user.id, user.roles)

        token = await TokenService().create_token(session=session)

        sanitazed_session = session.sanitaze()

        auth_result = AuthResult(
            session=sanitazed_session,
            access_token=token,
            refresh_token=session.refresh_token,
        )
        return auth_result
