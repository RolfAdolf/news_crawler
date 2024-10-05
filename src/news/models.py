from sqlalchemy import Column, Date, Integer, String, UniqueConstraint

from models import Base


class News(Base):
    __tablename__ = "news"
    __table_args__ = (UniqueConstraint("headline", "posted_at", name="news_headline_posted_at_uniq"),)

    id = Column(Integer, autoincrement=True, primary_key=True)
    headline = Column(String, nullable=False)
    photo = Column(String, nullable=True)
    posted_at = Column(Date, index=True, nullable=False)
