from utils.feed_sites import LIFE_HACKER
import feedparser
from dateutil import parser
from models.news import News
from utils.scrapped_news import scrapped


class LifeHackerSpider:
    def __init__(self) -> None:
        self.parse_and_notify()

    def parse_and_notify(self):
        feed = feedparser.parse(LIFE_HACKER)
        for entry in feed.entries:
            id = entry.id
            title = entry.title
            description = entry.description
            publish_date = parser.parse(entry.published)
            cover_image = entry.media_thumbnail[0]['url']
            link = entry.link

            news = News(id=id, title=title, description=description, publish_date=publish_date, cover_image=cover_image, link=link)
            scrapped.append(news)
            print(news.__str__())