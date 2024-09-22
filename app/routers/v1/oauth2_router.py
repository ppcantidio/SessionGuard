from fastapi import APIRouter

from app.models.oauth2_models import OAuth2Model
from app.services.injection_service import inject_dependencies
from app.usecases.oauth2 import OAuth2

router = APIRouter(tags=["Github"], prefix="/oauth2")


@router.post("", status_code=201)
async def oauth2_singup(payload: OAuth2Model):
    usecase = inject_dependencies(OAuth2)
    result = await usecase.execute(code=payload.code, provider=payload.provider)
    return result
