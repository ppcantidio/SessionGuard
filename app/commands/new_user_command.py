from pydantic import BaseModel
from app.models.enums import ProviderEnum
from typing import Optional

class NewUserCommand(BaseModel):
    provider: Optional[ProviderEnum]
    