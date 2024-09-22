from app.models.enums import ProviderEnum
from app.oauth2.github_oauth2 import GitHubOAuth2
from app.oauth2.google_oauth2 import GoogleOAuth2
from app.oauth2.oauth2_interface import OAuth2Interface
from app.results.auth_result import AuthResult
from app.services.auth_service import AuthService
from app.services.user_service import UserService


class OAuth2SingUp:
    def __init__(
        self,
        user_service: UserService,
        auth_service: AuthService,
    ):
        self.user_service = user_service
        self.auth_service = auth_service

    async def execute(self, provider: ProviderEnum, code: str) -> AuthResult:
        oauth2_impls = {
            ProviderEnum.github: GitHubOAuth2,
            ProviderEnum.google: GoogleOAuth2,
        }

        oauth2: OAuth2Interface = oauth2_impls[provider]()

        provider_token = await oauth2.get_token(code)

        provider_user = await oauth2.get_user(provider_token.access_token.token)

        await self._verify_user_by_provider_id(provider_user.id, provider)

        user = await self.user_service.create_user(
            email=provider_user.email,
            provider=provider,
            provider_id=provider_user.id,
        )

        auth_result = await self.auth_service.auth(user, provider_token)
        return auth_result

    async def _verify_user_by_provider_id(
        self, provider_id: str, provider: ProviderEnum
    ) -> bool:
        return True
