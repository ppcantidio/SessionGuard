import httpx

from app.config import app_config
from app.models.auth_models import ProviderTokens, Token
from app.oauth2_providers.models.github_models import GitHubUser
from app.oauth2_providers.oauth2_interface import OAuth2Interface, OAuth2User


class GitHubOAuth2(OAuth2Interface):
    async def get_token(self, code: str) -> ProviderTokens:
        url = "https://github.com/login/oauth/access_token"

        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                data={
                    "client_id": app_config.github_client_id,
                    "client_secret": app_config.github_client_secret,
                    "code": code,
                },
            )

            response.raise_for_status()

            token = response.json().get("access_token")
            access_token = Token(token=token)
            provider_tokens = ProviderTokens(access_token=access_token)
            return provider_tokens

    async def get_user(self, token: str) -> OAuth2User:
        url = "https://api.github.com/user"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"},
            )

            response.raise_for_status()

            json_response = response.json()

            github_user = GitHubUser(**json_response)
            oauth_user = OAuth2User(
                id=github_user.id,
                email=github_user.email,
            )
            return oauth_user
