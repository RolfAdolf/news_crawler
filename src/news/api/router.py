import logging
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends
from fastapi_utilities import repeat_every

from core.settings import crawler_settings
from database import get_async_session
from news.api.schemas import News
from news.crawler import NewsCrawler
from news.integration.transport import get_crawler_transport
from news.repo import NewsRepo
from news.service import NewsService


logger = logging.getLogger("default")


router = APIRouter(prefix="/news", tags=["News"])


@router.get("/")
async def define_team_for_student(days: int, news_service: NewsService = Depends(NewsService)) -> list[News]:
    news_list = await news_service.get_news_from_last_n_days(n=days)
    return [
        News(
            headline=news.headline,
            url=news.photo,
            date=news.posted_at,
        )
        for news in news_list
    ]


@router.on_event("startup")
@repeat_every(seconds=crawler_settings.aggregation_period, raise_exceptions=True)
async def run_crawler() -> None:
    client = get_crawler_transport()
    crawler = NewsCrawler(transport=client)
    news_list = await crawler.run()

    async with asynccontextmanager(get_async_session)() as session:
        repo = NewsRepo(session)
        await repo.bulk_insert_news(news_list=news_list)
