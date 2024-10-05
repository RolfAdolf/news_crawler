import datetime
import logging

from bs4 import BeautifulSoup
from httpx import AsyncClient

from news.dto import NewsDTO


logger = logging.getLogger("default")


class NewsCrawler:
    NEWS_URL = "/news/tags.php?metro"

    def __init__(self, transport: AsyncClient):
        self._transport = transport

    async def run(self) -> set[NewsDTO]:
        response = await self._transport.get(self.NEWS_URL)
        return self._parse_page(response.text)

    def _parse_page(self, page: str) -> set[NewsDTO]:
        news_list = self._get_raw_news(page=page)
        result = set()
        for news in news_list:
            try:
                result.add(
                    NewsDTO(
                        headline=self._extract_headline(news),
                        photo=self._extract_photo(news),
                        posted_at=self._extract_posted_at(news),
                    )
                )
            except Exception as parsing_exc:
                logger.info("Error parsing web page: %(err_mess)s", {"err_mess": str(parsing_exc)})
        return result

    @classmethod
    def _extract_headline(cls, raw_news: BeautifulSoup) -> str:
        return raw_news.find("font", {"size": "3"}).find("b").text

    @classmethod
    def _extract_photo(cls, raw_news: BeautifulSoup) -> str | None:
        if (im := raw_news.find("img")) is None:
            return None
        return im["src"]

    @classmethod
    def _extract_posted_at(cls, raw_news: BeautifulSoup) -> datetime.date:
        posted_at_str = raw_news.find("b").text
        return datetime.datetime.strptime(posted_at_str, "%d.%m.%Y").date()

    @classmethod
    def _get_raw_news(cls, page: str) -> list[BeautifulSoup]:
        soup = BeautifulSoup(page)
        return soup.find("table", {"width": "95%", "cellpadding": "0", "cellspacing": "10", "border": "0"}).findAll(
            "tr"
        )
