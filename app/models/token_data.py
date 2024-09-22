from datetime import datetime
from typing import List

from pydantic import UUID4, BaseModel


class TokenData(BaseModel):
    user_id: UUID4
    session_id: UUID4
    permissions: List[str]
    provider: str
    provider_user_id: str
    provider_expires_at: datetime
    exp: datetime
    iat: datetime
