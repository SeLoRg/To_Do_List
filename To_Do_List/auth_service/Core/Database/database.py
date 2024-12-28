from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from To_Do_List.Core.config.config import settings


class DataBase:
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


database = DataBase(url=settings.db_url, echo=settings.db_echo)
