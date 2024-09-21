from fastapi import APIRouter

router = APIRouter(tags=["Password"], prefix="/password")


@router.post("/reset")
async def request_password_reset():
    return {"message": "request password reset"}


@router.put("/reset")
async def password_reset():
    return {"message": "confirm password reset"}
