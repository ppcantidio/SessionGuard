from fastapi import APIRouter

router = APIRouter(tags=["Session"], prefix="/sessions")


@router.post("")
async def new_session():
    return {"message": "session"}


@router.post("")
async def get_all_sessions():
    return {"message": "sessions"}


@router.get("/{session_id}")
async def get_session(session_id: str):
    return {"message": "session"}


@router.delete("/{session_id}")
async def logout(session_id: str):
    return {"message": "logout"}


@router.post("/refresh")
async def refresh_session():
    return {"message": "refresh"}
