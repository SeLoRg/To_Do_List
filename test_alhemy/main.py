from test_alhemy.config import settings
import asyncio
from test_alhemy import config, models, database
from sqlalchemy import Result, select, update, delete, insert, text
from sqlalchemy.ext.asyncio import AsyncSession


async def main():
    async for session in database.db_helper.get_session():
        ses: AsyncSession = session

        stmt = select(models.WorkersModel.rang)
        res: Result = await ses.execute(stmt)
        print(res.scalars().all())
        print("\n----До-----\n")

        # stmt = text(
        #     """
        #             UPDATE "Workers"
        #             SET rang = 't1'
        #             WHere id = 2;
        #                 """
        # )
        stmt = (
            update(models.WorkersModel)
            .where(models.WorkersModel.id == 2)
            .values(rang="t1")
        )
        await ses.execute(stmt)

        print("\n----После-----\n")

        stmt = select(models.WorkersModel.rang)
        res: Result = await ses.execute(stmt)
        print(res.scalars().all())


asyncio.run(main())
# print(out)
# print(out.all())
# for i in out:
#     print(i)
