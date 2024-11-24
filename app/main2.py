from fastapi import FastAPI
from app.router import router
from api_v2 import router as api_router
from app.auth_jwt_router import router as jwt_router

app = FastAPI()
app.include_router(router, prefix="/auth", tags=["Authorize"])
app.include_router(api_router, prefix="/api_v2")
app.include_router(jwt_router, prefix="/jwt-auth")
