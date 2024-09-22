from app.gateways.github_gateway import GithubGateway
from app.models.enums import ProviderEnum
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


class GithubSingIn:
    def __init__(
        self,
        user_repository: UserRepository,
        github_gateway: GithubGateway,
        auth_service: AuthService,
    ):
        self.user_repository = user_repository
        self.github_gateway = github_gateway
        self.auth_service = auth_service

    async def execute(self, code: str):
        provider_token = await self.github_gateway.get_token(code)

        github_user = await self.github_gateway.get_user(
            provider_token.access_token.token
        )

        user = await self.user_repository.get_by_provider_id(
            str(github_user.id), ProviderEnum.github
        )
        if user is None:
            raise Exception("User not found")

        auth_result = await self.auth_service.auth(user, provider_token)
        return auth_result
