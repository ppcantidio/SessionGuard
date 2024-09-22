from sqlmodel import SQLModel, Field, UUID
from typing import Optional
from uuid import uuid4


class AppConfig(SQLModel, table=True):
    app_config_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    default_user_group_id: UUID = Field(foreign_key="group.group_id")
