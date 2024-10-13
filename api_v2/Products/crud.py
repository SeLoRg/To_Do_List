from typing import List
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from Core2.Models import ProductsModel
from api_v2.Products import (
    ProductsCreateSchema,
    ProductsUpdatePartialSchema,
    ProductsUpdateSchema,
)
from . import dependencies


async def get_products(session: AsyncSession) -> List[ProductsModel]:
    stmt = select(ProductsModel).order_by(ProductsModel.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(
    product_id: int,
    session: AsyncSession,
) -> ProductsModel | None:
    return await dependencies.product_by_id(product_id=product_id, session=session)


async def create_product(
    product_in: ProductsCreateSchema,
    session: AsyncSession,
) -> ProductsModel:
    product = ProductsModel(**product_in.model_dump())
    session.add(product)
    await session.commit()
    return product


async def update_product(
    product_in: ProductsUpdateSchema | ProductsUpdatePartialSchema,
    product: ProductsModel,
    session: AsyncSession,
    partial: bool = False,
) -> ProductsModel:
    for key, value in product_in.model_dump(exclude_none=partial).items():
        setattr(product, key, value)

    await session.commit()

    return product


async def delete_product(product: ProductsModel, session: AsyncSession) -> None:
    await session.delete(product)
    await session.commit()
