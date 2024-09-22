from typing import List, Optional
from uuid import uuid4

from models import Group
from sqlmodel import UUID, Field, Relationship, SQLModel


class User(SQLModel, table=True):
    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str
    email: str
    provider_name: Optional[str] = None
    provider_id: Optional[str] = None

    groups: List["Group"] = Relationship(back_populates="users")
