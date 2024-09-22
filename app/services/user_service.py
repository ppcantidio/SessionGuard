from typing import Optional

from app.models.enums import ProviderEnum
from app.models.user import User


class UserService:
    def __init__(self, user_repository, group_repository):
        self.user_repository = user_repository
        self.group_repository = group_repository

    async def create_user(
        self,
        email: Optional[str],
        hashed_password: Optional[str],
        provider: Optional[ProviderEnum] = None,
        provider_id: Optional[str] = None,
    ) -> dict:
        if email is not None:
            await self.verify_user_by_email(email)

        group = await self.get_default_group()

        user = User(
            email=email,
            hashed_password=hashed_password,
            provider_name=provider,
            provider_id=provider_id,
            groups=[group],
        )

        await self.user_repository.add(user)

        return user

    async def verify_user_by_email(self, email: str) -> bool:
        return True

    async def get_default_group_id(self) -> str:
        pass

    async def get_default_group(self) -> str:
        default_group_id = await self.get_default_group()
        group = await self.group_repository.get(default_group_id)
        return group
