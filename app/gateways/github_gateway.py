import httpx

from app.config import app_config
from app.gateways.models.github_models import GitHubUser
from app.models.auth_models import ProviderTokens, Token


class GithubGateway:
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

    async def get_user(self, token: str) -> GitHubUser:
        url = "https://api.github.com/user"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                headers={"Authorization": f"Bearer {token}"},
            )

            response.raise_for_status()

            json_response = response.json()

            github_user = GitHubUser(**json_response)
            return github_user
