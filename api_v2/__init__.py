from fastapi import APIRouter
from .Products.router import router as router_Products
from .User.router import router as router_User
from .Post.router import router as router_Post

router = APIRouter()
router.include_router(router=router_Products, prefix="/products")
router.include_router(router_User, prefix="/User")
router.include_router(router_Post, prefix="/Post")
