from app.services.auth_service import AuthService
from app.services.user_service import UserService
from teste import AuthResult


class AppSingUp:
    def __init__(self, user_service: UserService, auth_service: AuthService) -> None:
        self.user_service = user_service
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> AuthResult:
        hashed_password = await self.auth_service.encrypt_password(password)
        user = await self.user_service.create_user(
            email=email,
            hashed_password=hashed_password,
        )
        auth_result = await self.auth_service.auth(user)
        return auth_result
