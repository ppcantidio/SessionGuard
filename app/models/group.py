from typing import List, Optional
from uuid import uuid4

from models import Permission, User
from sqlmodel import UUID, Field, Relationship, SQLModel


class Group(SQLModel, table=True):
    group_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str
    description: str

    users: List["User"] = Relationship(back_populates="groups")
    permissions: List["Permission"] = Relationship(back_populates="groups")
