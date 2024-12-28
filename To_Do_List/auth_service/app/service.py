from .shemas import UserLoginSchema
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response, HTTPException, status
from .jwt_factory import issue_tokens

from .kafka_interaction import get_user_from_users_service


async def login_user(
    data: UserLoginSchema,
    session: AsyncSession,
    response: Response,
) -> dict[str, str]:
    user_id: int = await get_user_from_users_service(email=data.email)
    await issue_tokens(session=session, user_id=user_id, response=response)

    return {"detail": f"user: {data.email} login successfully"}
