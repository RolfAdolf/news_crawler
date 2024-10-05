import datetime

from pydantic import BaseModel, Field


class News(BaseModel):
    headline: str = Field(..., description="Заголовок новости")
    url: str = Field(..., description="URL картинки новости")
    date: datetime.date = Field(..., description="Дата публикации")
