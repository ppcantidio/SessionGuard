from app.models.enums import ProviderEnum
from app.oauth2_providers.github_oauth2 import GitHubOAuth2
from app.oauth2_providers.google_oauth2 import GoogleOAuth2
from app.oauth2_providers.oauth2_interface import OAuth2Interface
from app.repositories.user_repository import UserRepository
from app.results.auth_result import AuthResult
from app.services.auth_service import AuthService
from app.services.user_service import UserService


class OAuth2:
    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthService,
        user_service: UserService,
    ):
        self.user_service = user_service
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def execute(self, provider: ProviderEnum, code: str) -> AuthResult:
        oauth2_impls = {
            ProviderEnum.github: GitHubOAuth2,
            ProviderEnum.google: GoogleOAuth2,
        }

        oauth2: OAuth2Interface = oauth2_impls[provider]()

        provider_token = await oauth2.get_token(code)
        user_provider = await oauth2.get_user(provider_token.access_token.token)

        user = await self.user_repository.get_by_provider_id(user_provider.id, provider)
        if user is None:
            # SingUp
            user = await self.user_service.create_user(
                email=user_provider.email,
                provider=provider,
                provider_id=user_provider.id,
            )

        auth_result = await self.auth_service.auth(
            user, provider, provider_token, user_provider
        )
        return auth_result
