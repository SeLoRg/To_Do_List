from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./db_sqlite.db"
    db_echo: bool = False


settings = Settings()
