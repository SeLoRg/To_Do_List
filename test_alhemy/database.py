from test_alhemy.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession


class DatBaseHelper:
    def __init__(self, url, echo):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as sess:
            yield sess
            await sess.close()


db_helper = DatBaseHelper(url=settings.db_url, echo=True)
