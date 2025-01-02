from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings

load_dotenv("../.env")


class DBSettings(BaseSettings):
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    db_echo: bool = False

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}"


class Settings(DBSettings):
    pass


settings = Settings()
