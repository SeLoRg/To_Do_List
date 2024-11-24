import datetime

from dotenv import load_dotenv
import os
from fastapi_mail import ConnectionConfig
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pathlib import Path

load_dotenv("C:/Users/rosti/PycharmProjects/FastAPI_DB/To_Do_List/.env")


class AuthJWT(BaseModel):
    private_key: Path = Path(
        "C:/Users/rosti/PycharmProjects/FastAPI_DB/certs/jwt-private.pem"
    )
    publik_key: Path = Path(
        "C:/Users/rosti/PycharmProjects/FastAPI_DB/certs/jwt-public.pem"
    )
    algorithm: str = "RS256"
    token_refresh_live: datetime.datetime = datetime.timedelta(days=1)
    token_access_live: datetime.datetime = datetime.timedelta(minutes=15)


class SMTPSettings(BaseSettings):
    MAIL_KEY: str = os.environ.get("MAIL_KEY")
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME")
    MAIL_FROM: str = os.environ.get("MAIL_FROM")
    MAIL_PORT: str = os.environ.get("MAIL_PORT")
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER")
    MAIL_FROM_NAME: str = os.environ.get("MAIL_FROM_NAME")
    MAIL_STARTTLS: str = os.environ.get("MAIL_STARTTLS")
    MAIL_SSL_TLS: str = os.environ.get("MAIL_SSL_TLS")

    @property
    def smtp_conf(self) -> ConnectionConfig:
        return ConnectionConfig(
            MAIL_USERNAME=self.MAIL_USERNAME,
            MAIL_PASSWORD=self.MAIL_KEY,
            MAIL_FROM=self.MAIL_FROM,
            MAIL_PORT=int(self.MAIL_PORT),
            MAIL_SERVER=self.MAIL_SERVER,
            MAIL_FROM_NAME=self.MAIL_FROM_NAME,
            MAIL_STARTTLS=bool(int(self.MAIL_STARTTLS)),
            MAIL_SSL_TLS=bool(int(self.MAIL_SSL_TLS)),
        )


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


class Settings(SMTPSettings, DBSettings):
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
