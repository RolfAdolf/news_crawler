import logging
import os
from pathlib import Path

from pydantic import Field

from pydantic_settings import BaseSettings


logger = logging.getLogger("info")


BASE_DIR = Path(os.getcwd())


DEBUG = int(os.environ.get("DEBUG", 0))


class AppSettings(BaseSettings):
    app_host: str = "0.0.0.0"  # noqa: S104
    app_port: int = 8888


class CrawlerSettings(BaseSettings):
    request_timeout: int = 60
    aggregation_period: int = 60 * 10


class DatabaseSettings(BaseSettings):
    db: str = Field(..., alias="database_db")
    password: str = Field(..., alias="database_password")
    user: str = Field(..., alias="database_user")
    host: str = Field(..., alias="database_host")
    port: str = Field(..., alias="database_port")

    @property
    def dsn(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db}"


app_settings = AppSettings()
crawler_settings = CrawlerSettings()
db_settings = DatabaseSettings()
