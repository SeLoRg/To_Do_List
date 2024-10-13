from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from Core2.Models import ProductsModel
from Core2.db_helper import db_helper
from starlette import status


async def product_by_id(
    product_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
) -> ProductsModel | None:
    product: ProductsModel | None = await session.get(ProductsModel, product_id)
    if product is not None:
        return product
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
