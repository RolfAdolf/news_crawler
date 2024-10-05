import datetime

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from news.dto import NewsDTO
from news.models import News


class NewsRepo:
    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session = session

    async def get_news_since_date(self, date: datetime.date) -> list[NewsDTO]:
        query = select(News).where(News.posted_at >= date).order_by(News.posted_at.desc())
        result = await self._session.execute(query)
        return [
            NewsDTO(
                headline=news.headline,
                photo=news.photo,
                posted_at=news.posted_at,
            )
            for news in result.scalars().all()
        ]

    async def bulk_insert_news(self, news_list: set[NewsDTO]) -> None:
        insert_stmt = Insert(News).values([news.model_dump() for news in news_list])
        query = insert_stmt.on_conflict_do_update(
            constraint="news_headline_posted_at_uniq",
            set_={"photo": insert_stmt.excluded.photo},
        )
        await self._session.execute(query)
        await self._session.commit()
