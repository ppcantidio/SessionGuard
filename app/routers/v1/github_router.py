from fastapi import APIRouter

router = APIRouter(tags=["Github"], prefix="/github")


@router.post("/callback")
async def github_callback():
    return {"message": "github callback"}
