import logging

from fastapi import FastAPI

from core.logging_config import setup_logging
from news.api.router import router as news_router


logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app_ = FastAPI()
    app_.include_router(news_router)
    return app_


app = create_app()


@app.on_event("startup")
async def startup() -> None:
    await setup_logging()
