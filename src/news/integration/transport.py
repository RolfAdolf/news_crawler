import logging

import httpx

from core.settings import crawler_settings
from news.integration.exceptions import CrawlerHttpRequestError


logger = logging.getLogger("default")


async def response_handler(response: httpx.Response) -> None:
    log_level = logging.ERROR if response.status_code >= 400 else logging.INFO
    logger.log(
        log_level,
        "Request url: %(url)s, method: %(method)s, status: %(status_code)d.",
        {
            "url": response.url,
            "method": response.request.method,
            "status_code": response.status_code,
        },
    )

    await response.aread()

    if 300 <= response.status_code <= 399:
        return

    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as err:
        raise CrawlerHttpRequestError(
            err.response.status_code,
            err.response.text,
        )


def get_crawler_transport() -> httpx.AsyncClient:
    return httpx.AsyncClient(
        base_url="http://mosday.ru",
        verify=False,  # noqa: S501
        timeout=crawler_settings.request_timeout,
        event_hooks={
            "response": [response_handler],
        },
        follow_redirects=True,
    )
