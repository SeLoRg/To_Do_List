from test_alhemy.config import settings
import asyncio
from test_alhemy import config, database
from sqlalchemy import Result, select, update, delete, insert, text, func, cast, Integer
from sqlalchemy.orm import joinedload, selectinload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession
from models import (
    ResumesModel,
    WorkersModel,
    Workload,
    OrdersModel,
    OrderProduct,
    ProductsModel,
)


async def main():
    async for session in database.db_helper.get_session():
        ses: AsyncSession = session

        stmt = (
            select(OrdersModel)
            .options(selectinload(OrdersModel.products))
            .order_by(OrdersModel.id)
        )
        orders = await ses.execute(stmt)
        orders = orders.scalars().all()

        for i in orders:
            for j in i.products:
                print(j)

        return 1


out = asyncio.run(main())
