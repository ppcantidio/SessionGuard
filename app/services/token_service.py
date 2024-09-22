from datetime import datetime, timedelta

import jwt

from app.config import app_config
from app.models import Session, TokenData
from app.models.auth_models import Token


class TokenService:
    async def create_token(self, session: Session) -> Token:
        iat = datetime.now()
        exp = iat + timedelta(minutes=app_config.access_token_lifetime_minutes)

        token_data = TokenData(
            session_id=session.session_id, user=session.user, exp=exp, iat=iat
        )
        token_dict = token_data.model_dump(mode="json")

        encoded_jwt = jwt.encode(
            token_dict, app_config.secret_key, algorithm=app_config.algorithm
        )
        return Token(token=encoded_jwt, expires_at=exp)

    async def decode_token(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, app_config.secret_key, algorithms=[app_config.algorithm]
            )
            return TokenData(**payload)
        except jwt.PyJWTError:
            raise Exception("Could not validate credentials")
