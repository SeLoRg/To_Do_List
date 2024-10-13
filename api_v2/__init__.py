from fastapi import APIRouter
from .Products.router import router as router_v1


router = APIRouter()
router.include_router(router=router_v1, prefix="/products")
