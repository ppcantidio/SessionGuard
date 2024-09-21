from app.services.session_service import SessionService
from app.config import app_config

class AuthSession:
    async def execute(self, username: str, password: str):
        session_service = SessionService(redis_url=app_config.redis_url)
        
        user = await user_repository.get_user_by_username(username)
        
        if not user:
            raise Exception("User not found")
        
        is_valid = await user.check_password(password)
        
        if not is_valid:
            raise Exception("Invalid password")
        
        session = await session_service.create_session(user.id, user.roles)
        
        return session
        