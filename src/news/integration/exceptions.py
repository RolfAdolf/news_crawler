class CrawlerHttpRequestError(Exception):
    def __init__(self, status_code: int, error_info: str):
        self._status_code = status_code
        self._error_info = error_info
        super().__init__()

    def __str__(self) -> str:
        return f"{self._status_code}: {self._error_info}"
