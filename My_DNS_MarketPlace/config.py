from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

import os


load_dotenv(
    dotenv_path="C:/Users/rosti/PycharmProjects/FastAPI_DB/My_DNS_MarketPlace/.env"
)


class Settings(BaseSettings):
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_HOST: str = os.environ.get("DB_HOST")

    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file="C:/Users/rosti/PycharmProjects/FastAPI_DB/My_DNS_MarketPlace/.env"
    )

    db_echo: bool = False


settings = Settings()
