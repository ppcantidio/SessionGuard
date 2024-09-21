from fastapi import APIRouter

router = APIRouter(tags=["Permission"], prefix="/permissions")


@router.post("/")
async def new_permission():
    return {"message": "permission"}


@router.get("/{permission_id}")
async def get_permission(permission_id: str):
    return {"message": "permission"}


@router.delete("/{permission_id}")
async def delete_permission(permission_id: str):
    return {"message": "permission"}
