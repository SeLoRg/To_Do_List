import asyncio

import sqlalchemy_h.config
from sqlalchemy_h.models import WorkersModel
from database import db_helper
from sqlalchemy import insert

# from sqlalchemy.ext.asyncio import AsyncSession


# from config import settings

# print(settings.db_url)


async def main():
    # session = db_helper.get_session()
    # async for ses in session:
    #     worker_in = WorkersModel(name="Nastya", rang="Student")
    #     ses.add(worker_in)
    #     await ses.commit()
    print(sqlalchemy_h.config.settings.db_url)
    a = WorkersModel(name="ros", rang="t5")
    print(a)


asyncio.run(main())
