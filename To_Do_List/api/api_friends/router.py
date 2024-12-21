from fastapi import APIRouter


router = APIRouter(tags=["Friends"], prefix="/friends")


@router.post("/send-request-friends")
async def send_request_friends():
    pass
