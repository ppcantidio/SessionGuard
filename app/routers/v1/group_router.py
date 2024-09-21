from fastapi import APIRouter

router = APIRouter(tags=["Group"], prefix="/groups")


@router.post("/")
async def new_group():
    return {"message": "group"}


@router.get("/{group_id}")
async def get_group(group_id: str):
    return {"message": "group"}


@router.delete("/{group_id}")
async def delete_group(group_id: str):
    return {"message": "group"}
