from contextlib import asynccontextmanager
from fastapi import FastAPI
from Core.Models import db_helper, Base
from Core.config import settings
from app.router import router
from api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


# app = FastAPI()
app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(router_v1, prefix=settings.api_v1_prefix)
