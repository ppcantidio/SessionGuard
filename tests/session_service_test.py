import json
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from app.models.auth_models import Session
from app.models.token_data import TokenData
from app.services.session_service import SessionService


@pytest.fixture
def mock_redis():
    with patch("redis.asyncio.from_url", return_value=AsyncMock()) as mock:
        yield mock


@pytest.fixture
def session_service(mock_redis):
    return SessionService(redis_url="redis://localhost")


@pytest.mark.asyncio
async def test_create_token(session_service: SessionService):
    iat_datetime = datetime.fromtimestamp(int(datetime.now().timestamp()))
    exp_datetime = iat_datetime + timedelta(seconds=3600)
    exp_datetime = datetime.fromtimestamp(int(exp_datetime.timestamp()))

    token_data = TokenData(
        user_id=uuid4(),
        session_id=uuid4(),
        roles=["user"],
        exp=exp_datetime,
        iat=iat_datetime,
    )

    token = await session_service.create_token(token_data)
    result = await session_service.decode_token(token)

    assert result == token_data


@pytest.mark.asyncio
async def test_create_session(session_service):
    user_id = uuid4()
    roles = ["user"]
    ttl_seconds = 3600

    token_data = await session_service.create_session(user_id, roles, ttl_seconds)

    assert token_data.user_id == user_id
    assert token_data.roles == roles
    assert token_data.exp > datetime.now()
    assert token_data.iat < datetime.now()


@pytest.mark.asyncio
async def test_get_session(session_service, mock_redis):
    user_id = uuid4()
    session_id = uuid4()
    token_data = TokenData(
        user_id=user_id,
        session_id=session_id,
        roles=["user"],
        exp=datetime.now() + timedelta(seconds=3600),
        iat=datetime.now(),
    )

    session_service.redis.get = AsyncMock(return_value="token")
    session_service.decode_token = AsyncMock(return_value=token_data)

    result = await session_service.get_session(session_id, user_id)

    assert result.user_id == user_id
    assert result.session_id == session_id
    assert result.roles == ["user"]


@pytest.mark.asyncio
async def test_logout(session_service, mock_redis):
    user_id = uuid4()
    session_id = uuid4()

    await session_service.logout(session_id, user_id)

    mock_redis.delete.assert_called_once_with(f"session:{user_id}:{session_id}")


@pytest.mark.asyncio
async def test_get_all_sessions(session_service, mock_redis):
    user_id = uuid4()
    session_id = uuid4()
    session_data = Session(
        user_id=user_id,
        session_id=session_id,
        roles=["user"],
        exp=datetime.now() + timedelta(seconds=3600),
        iat=datetime.now(),
    )
    mock_redis.keys.return_value = [f"session:{user_id}:{session_id}"]
    mock_redis.get.return_value = json.dumps(session_data.model_dump())

    result = await session_service.get_all_sessions(user_id)

    assert len(result) == 1
    assert result[0].user_id == user_id
    assert result[0].session_id == session_id


@pytest.mark.asyncio
async def test_logout_all(session_service, mock_redis):
    user_id = uuid4()
    session_id = uuid4()
    mock_redis.keys.return_value = [f"session:{user_id}:{session_id}"]

    await session_service.logout_all(user_id)

    mock_redis.delete.assert_called_once_with(f"session:{user_id}:{session_id}")
