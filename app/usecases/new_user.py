from app.commands.new_user_command import NewUserCommand
from app.models import User


class NewUser:
    async def execute(self, command: NewUserCommand):
        user = User(
            username=command.username,
            password=command.password,
            roles=command.roles,
        )

        await user.save()
        return user
