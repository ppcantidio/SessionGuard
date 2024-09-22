from app.models.enums import ProviderEnum
from app.oauth2.github_oauth2 import GitHubOAuth2
from app.oauth2.google_oauth2 import GoogleOAuth2
from app.oauth2.oauth2_interface import OAuth2Interface
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


class OAuth2SingIn:
    def __init__(
        self,
        user_repository: UserRepository,
        auth_service: AuthService,
    ):
        self.user_repository = user_repository
        self.auth_service = auth_service

    async def execute(self, provider: ProviderEnum, code: str):
        oauth2_impls = {
            ProviderEnum.github: GitHubOAuth2,
            ProviderEnum.google: GoogleOAuth2,
        }

        oauth2: OAuth2Interface = oauth2_impls[provider]()

        provider_token = await oauth2.get_token(code)
        user_provider = await oauth2.get_user(provider_token.access_token.token)

        user = await self.user_repository.get_by_provider_id(user_provider.id, provider)
        if user is None:
            raise Exception("User not found")

        auth_result = await self.auth_service.auth(user, provider_token)
        return auth_result
