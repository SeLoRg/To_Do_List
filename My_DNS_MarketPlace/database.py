from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from My_DNS_MarketPlace.config import settings


class DataBaseHelper:
    def __init__(self, url, echo):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            self.engine, autoflush=False, autocommit=False
        )

    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as sess:
            yield sess

            await sess.close()


db_helper = DataBaseHelper(url=settings.db_url, echo=settings.db_echo)
