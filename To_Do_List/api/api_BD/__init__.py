from fastapi import APIRouter
from .users.router import router as users_router
from .todoes.router import router as todo_router

router = APIRouter(prefix="/api-bd")
router.include_router(router=users_router, prefix="/users")
router.include_router(router=todo_router, prefix="/tasks")
