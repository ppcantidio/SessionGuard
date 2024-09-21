from datetime import datetime
from typing import List

from pydantic import UUID4, BaseModel


class TokenData(BaseModel):
    user_id: UUID4
    session_id: UUID4
    roles: List[str]
    exp: datetime
    iat: datetime
