from typing import List, Optional
from uuid import uuid4

from models import Group
from pydantic import model_validator
from sqlmodel import UUID, Field, Relationship, SQLModel


class User(SQLModel, table=True):
    user_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    email: str
    hashed_password: Optional[str] = None
    provider_name: Optional[str] = None
    provider_id: Optional[str] = None

    groups: List["Group"] = Relationship(back_populates="users")

    @model_validator
    def check_credentials(cls, values):
        email = values.get("email")
        hashed_password = values.get("hashed_password")
        provider_name = values.get("provider_name")
        provider_id = values.get("provider_id")

        if (email and hashed_password) or (provider_name and provider_id):
            return values

        if provider_id and not provider_name:
            raise ValueError(
                "If provider_id is provided, provider_name must also be provided."
            )
        if provider_name and not provider_id:
            raise ValueError(
                "If provider_name is provided, provider_id must also be provided."
            )

        raise ValueError(
            "User must have either email and hashed_password, or provider_name and provider_id."
        )
