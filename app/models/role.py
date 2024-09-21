from typing import List

from models import User
from sqlmodel import Relationship, SQLModel


class Role(SQLModel, table=True):
    name: str
    description: str

    users: List["User"] = Relationship(back_populates="roles")
