from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from ..config.config import settings


class DataBase:
    def __init__(self, url, echo):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            pool_size=3,
            max_overflow=6,
            pool_recycle=250,
            pool_pre_ping=True,
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
        )

    async def get_session(self) -> AsyncSession:
        async with self.session_factory() as sess:
            yield sess


database_users = DataBase(url=settings.users_db_url, echo=settings.db_echo)
database_sessions = DataBase(url=settings.sessions_db_url, echo=settings.db_echo)
