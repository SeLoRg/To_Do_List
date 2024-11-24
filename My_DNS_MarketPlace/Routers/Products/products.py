from fastapi import APIRouter, Depends
from My_DNS_MarketPlace.BD_Models.Products import ProductsOrm
from sqlalchemy.ext.asyncio import AsyncSession
from My_DNS_MarketPlace.Schemas.products import ProductsPostSchema, ProductsGetSchema
from My_DNS_MarketPlace.database import db_helper
from My_DNS_MarketPlace.config import settings

router = APIRouter(tags=["Products"], prefix="/products")


@router.post("/")
async def post_product(
    product_in: ProductsPostSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    product = ProductsOrm(**product_in.model_dump())

    session.add(product)

    await session.commit()

    return product
