from fastapi import FastAPI

from .routers import router, producer

app = FastAPI()
app.include_router(router=router)


@app.on_event("startup")
async def startup_event():
    await producer.start()


@app.on_event("shutdown")
async def shutdown_event():
    await producer.stop()
