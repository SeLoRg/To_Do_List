import datetime

from dotenv import load_dotenv
import os
from pydantic_settings import BaseSettings
from pathlib import Path


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path)


class AuthJWT(BaseSettings):
    COOKIE_JWT_REFRESH: str = os.environ.get("COOKIE_JWT_REFRESH")
    COOKIE_JWT_ACCESS: str = os.environ.get("COOKIE_JWT_ACCESS")


class Settings(AuthJWT):
    pass


settings = Settings()
