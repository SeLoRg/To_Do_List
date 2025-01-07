from Core.config import settings
from Core.Database.database import database_sessions, database_users
import asyncio
from Core.Models import SessionsOrm, UsersOrm


async def test():
    s_u = database_users.get_session()
    s_s = database_sessions.get_session()

    async for conn in s_u:
        await conn.get(UsersOrm, 1)


asyncio.run(test())
