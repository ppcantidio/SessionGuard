from fastapi import APIRouter

from app import __version__

router = APIRouter(tags=["Healthcheck"])

_INFO = {"applicacao": __version__.__title__, "versao": __version__.__version__}


@router.get("/healthcheck")
async def health():
    return _INFO
