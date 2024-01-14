from datetime import datetime
from pydantic import BaseModel

class News(BaseModel):
    id: str
    title: str
    description: str
    publish_date: datetime
    cover_image: str
    link: str
