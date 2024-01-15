from datetime import datetime

from pydantic import BaseModel


class News(BaseModel):
    article_id: str
    title: str
    description: str
    publish_date: datetime
    cover_image: str
    link: str
