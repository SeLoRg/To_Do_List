from fastapi import APIRouter
from .Products.router import router as router_Products
from .User.router import router as router_User


router = APIRouter()
router.include_router(router=router_Products, prefix="/products")
router.include_router(router_User, prefix="/User")
