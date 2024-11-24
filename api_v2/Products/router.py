from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from Core2.db_helper import db_helper
from . import crud
from api_v2.Products import (
    ProductsCreateSchema,
    ProductsSchema,
    ProductsUpdatePartialSchema,
    ProductsUpdateSchema,
)
from typing import List
from Core2.Models import ProductsModel
from . import dependencies

router = APIRouter(tags=["Products"])


@router.get("/", response_model=List[ProductsSchema])
async def get_products(
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.get_products(session=session)


@router.get("/{product_id}/", response_model=ProductsSchema | None)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.get_product(product_id=product_id, session=session)


@router.post("/", response_model=ProductsSchema)
async def create_product(
    product_in: ProductsCreateSchema,
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.create_product(product_in=product_in, session=session)


@router.post("/{product_id}/", response_model=ProductsSchema)
async def update_product(
    product_in: ProductsUpdateSchema,
    product: ProductsModel = Depends(dependencies.product_by_id),
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.update_product(
        product=product, session=session, product_in=product_in
    )


@router.patch("/{product_id}/", response_model=ProductsSchema)
async def update_partial_product(
    product_in: ProductsUpdatePartialSchema,
    product: ProductsModel = Depends(dependencies.product_by_id),
    session: AsyncSession = Depends(db_helper.get_session),
):
    return await crud.update_product(
        product_in=product_in, product=product, session=session, partial=True
    )


@router.delete("/{product_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    session: AsyncSession = Depends(db_helper.get_session),
    product: ProductsModel = Depends(dependencies.product_by_id),
):
    await crud.delete_product(product=product, session=session)
