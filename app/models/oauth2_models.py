from pydantic import BaseModel

from app.models.enums import ProviderEnum


class OAuth2Model(BaseModel):
    code: str
    provider: ProviderEnum
