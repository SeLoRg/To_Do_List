from contextlib import asynccontextmanager

from Core2.Models import Base
from Core2.db_helper import db_helper
from fastapi import FastAPI
from app.router import router
from api_v2 import router as api_products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # async with db_helper.engine.begin() as eng:
    #     await eng.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.include_router(api_products_router, prefix="/api_v2")
