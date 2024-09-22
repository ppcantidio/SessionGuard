from app.gateways.github_gateway import GithubGateway
from app.results.auth_result import AuthResult
from app.services.auth_service import AuthService
from app.services.user_service import UserService


class GitHubSingUp:
    def __init__(
        self,
        github_gateway: GithubGateway,
        user_service: UserService,
        auth_service: AuthService,
    ):
        self.github_gateway = github_gateway
        self.user_service = user_service
        self.auth_service = auth_service

    async def execute(self, code: str) -> AuthResult:
        provider_token = await self.github_gateway.get_token(code)

        github_user = await self.github_gateway.get_user(
            provider_token.access_token.token
        )

        await self._verify_user_by_github_id(str(github_user.id))

        user = await self.user_service.create_user(
            username=github_user.login,
            email=github_user.email,
            password=None,
            roles=["user"],
        )

        auth_result = await self.auth_service.auth(user, provider_token)
        return auth_result

    async def _verify_user_by_github_id(self, github_id: str) -> bool:
        return True
