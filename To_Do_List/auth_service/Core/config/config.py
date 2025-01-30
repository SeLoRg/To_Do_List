import datetime

from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)


class AuthJWT(BaseSettings):
    private_key: Path = Path(
        "C:/Users/rosti/PycharmProjects/FastAPI_DB/certs/private_key.pem"
    )
    public_key: Path = Path(
        "C:/Users/rosti/PycharmProjects/FastAPI_DB/certs/public_key.pem"
    )
    algorithm: str = "RS256"
    token_refresh_live: datetime.timedelta = datetime.timedelta(days=30)
    token_access_live: datetime.timedelta = datetime.timedelta(minutes=5)

    COOKIE_JWT_REFRESH: str = os.environ.get("COOKIE_JWT_REFRESH")
    COOKIE_JWT_ACCESS: str = os.environ.get("COOKIE_JWT_ACCESS")


class DBSettings(BaseSettings):
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME_USERS: str = os.environ.get("DB_NAME_USERS")
    DB_NAME_SESSIONS: str = os.environ.get("DB_NAME_SESSIONS")

    db_echo: bool = True

    @property
    def users_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME_USERS}"

    @property
    def sessions_db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME_SESSIONS}"


class KafkaSettings(BaseSettings):
    KAFKA_BROKER: str = os.environ.get("KAFKA_BROKER")
    SERVICE_NAME: str = os.environ.get("SERVICE_NAME")


class RedisSettings(BaseSettings):
    REDIS_HOST: str = os.environ.get("REDIS_HOST")
    REDIS_PORT: str = os.environ.get("REDIS_PORT")
    REDIS_DB: str = os.environ.get("REDIS_DB")

    KEY_USER_SESSION: str = "session_"
    KEY_USER: str = "user_"


class Settings(DBSettings, KafkaSettings, AuthJWT, RedisSettings):
    pass


settings = Settings()
