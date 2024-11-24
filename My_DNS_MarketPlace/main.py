from fastapi import FastAPI
from My_DNS_MarketPlace.Routers import router


app = FastAPI()
app.include_router(router)
