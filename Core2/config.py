from pathlib import Path

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
from pydantic import BaseModel

load_dotenv()


class AuthJWT(BaseModel):
    private_key: Path = Path(
        "C:/Users/rosti/PycharmProjects/FastAPI_DB/certs/jwt-private.pem"
    )

    public_key: Path = Path(
        "C:/Users/rosti/PycharmProjects/FastAPI_DB/certs/jwt-public.pem"
    )
    algorithm: str = "RS256"


class Settings(BaseSettings):
    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PORT: str = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    DB_PASS: str = os.environ.get("DB_PASS")
    auth_jwt: AuthJWT = AuthJWT()

    # db_url: str = "sqlite+aiosqlite:///./db_sqlite.db"
    @property
    def db_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    db_echo: bool = False


settings = Settings()
