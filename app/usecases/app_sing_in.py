from app.exceptions import InvalidPassword, UserNotFound
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from teste import AuthResult


class AppSingIn:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> AuthResult:
        user = self.user_repository.get_by_email(email)
        if not user:
            raise UserNotFound()

        password_is_correct = await self.auth_service.check_password(user, password)
        if not password_is_correct:
            raise InvalidPassword()

        auth_result = await self.auth_service.auth(user)
        return auth_result
