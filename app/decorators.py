import functools

from app.exceptions import InvalidToken, SessionExpired
from app.services.injection_service import inject_dependencies
from app.usecases.check_auth import CheckAuth


def require_session():
    """
    Decorator to validate session and inject the sanitized session into the decorated function.
    """

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, token: str, **kwargs):
            try:
                check_auth: CheckAuth = inject_dependencies(CheckAuth)
                session = await check_auth.execute(token)
                return await func(*args, session=session, **kwargs)
            except SessionExpired:
                raise SessionExpired("Session has expired. Please log in again.")
            except InvalidToken:
                raise InvalidToken("Invalid token provided.")

        return wrapper

    return decorator
