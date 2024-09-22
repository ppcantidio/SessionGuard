from app.commands.new_user_command import NewUserCommand
from app.models import User

class NewUser:
    async def execute(self, command: NewUserCommand):
        pass
        