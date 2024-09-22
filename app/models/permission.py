from typing import Optional
from uuid import uuid4

from sqlmodel import UUID, Field, SQLModel


class Permission(SQLModel, table=True):
    permission_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str
