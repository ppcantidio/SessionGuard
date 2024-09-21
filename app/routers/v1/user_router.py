from fastapi import APIRouter

router = APIRouter(tags=["User"], prefix="/users")


@router.post("/")
async def new_user():
    return {"message": "user"}


@router.get("/me")
async def get_authenticated_user():
    return {"message": "Me"}


@router.put("/me/passoword")
async def change_authenticated_user_password():
    return {"message": "Change password"}
