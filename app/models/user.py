from typing import List, Optional

from models import Role
from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str

    roles: List["Role"] = Relationship(back_populates="users")
