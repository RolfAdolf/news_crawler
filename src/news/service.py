import datetime

from dateutil.relativedelta import relativedelta
from fastapi import Depends

from news.dto import NewsDTO
from news.repo import NewsRepo


class NewsService:

    def __init__(self, repo: NewsRepo = Depends(NewsRepo)):
        self._repo = repo

    async def get_news_from_last_n_days(self, n: int) -> list[NewsDTO]:
        curr_date = datetime.datetime.now(tz=datetime.timezone.utc).date()
        return await self._repo.get_news_since_date(date=curr_date - relativedelta(days=n))
