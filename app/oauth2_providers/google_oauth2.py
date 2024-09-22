from datetime import datetime, timedelta

import httpx

from app.config import app_config
from app.models.auth_models import ProviderTokens, Token
from app.oauth2_providers.models.google_models import GoogleUser
from app.oauth2_providers.oauth2_interface import OAuth2Interface, OAuth2User


class GoogleOAuth2(OAuth2Interface):
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_token(self, code: str) -> ProviderTokens:
        url = "https://oauth2.googleapis.com/token"
        response = await self.client.post(
            url,
            data={
                "code": code,
                "client_id": app_config.google_client_id,
                "client_secret": app_config.google_client_secret,
                "redirect_uri": app_config.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )

        response.raise_for_status()

        token = response.json().get("access_token")
        expires_in = response.json().get("expires_in")
        expires_at = datetime.now() + timedelta(seconds=expires_in)
        access_token = Token(token=token, expires_at=expires_at)
        provider_tokens = ProviderTokens(access_token=access_token)
        return provider_tokens

    async def get_user(self, token: str) -> OAuth2User:
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        response = await self.client.get(
            url,
            headers={"Authorization": f"Bearer {token}"},
        )

        response.raise_for_status()

        json_response = response.json()

        google_user = GoogleUser(**json_response)
        oauth_user = OAuth2User(
            id=google_user.id,
            email=google_user.email,
        )
        return oauth_user
