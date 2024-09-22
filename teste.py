import json
from datetime import datetime
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

T = TypeVar("T", bound=BaseModel)


class AuthResult(BaseModel):
    model_config = ConfigDict(
        json_encoders={datetime: lambda v: int(v.timestamp())}, strict=False
    )
    teste: datetime


class Result(BaseModel, Generic[T]):
    model_config = ConfigDict(json_encoders={datetime: lambda v: str(v)}, strict=False)
    data: T


result = AuthResult(teste=1726973487)
dados = Result(data=result.model_dump())

print(dados.model_dump(mode="json"))
