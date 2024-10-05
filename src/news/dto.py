import datetime

from pydantic import BaseModel


class NewsDTO(BaseModel):
    headline: str
    photo: str | None
    posted_at: datetime.date

    def __hash__(self) -> int:
        return (self.headline, self.posted_at).__hash__()

    def __eq__(self, other: "NewsDTO") -> bool:
        return self.headline == other.headline and self.posted_at == other.posted_at
