import asyncio

from fastapi import FastAPI
from .router import router
from redis import Redis
from redis.exceptions import ConnectionError
from ..Core.config import settings
from ..Core.Database.database import database_sessions, database_users
from sqlalchemy import text
from ..Core.redis_client.redis_client import redis_client

app = FastAPI()


app.include_router(router=router)


@app.on_event("startup")
async def startup_event():
    try:
        await redis_client.ping()
        async for sess in database_sessions.get_session():
            await sess.execute(text("SELECT 1"))

        async for sess in database_users.get_session():
            await sess.execute(text("SELECT 1"))
    except ConnectionError as e:
        print(f"Failed to connect to Redis: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    await asyncio.gather(
        database_users.engine.dispose(),
        database_sessions.engine.dispose(),
        redis_client.close(),
        return_exceptions=True,
    )
    print("shutdown ok")
