from fastapi import APIRouter
from My_DNS_MarketPlace.Routers.Products.products import router as product_router

router = APIRouter(prefix="/api")
router.include_router(product_router)
