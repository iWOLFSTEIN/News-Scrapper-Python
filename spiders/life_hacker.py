from spiders.spider import Spider
import feedparser
from dateutil import parser
from models.news import News


class LifeHackerSpider(Spider):
    def parse(self):
        feed = feedparser.parse(self.config.feed_urls.life_hacker)
        for entry in feed.entries:
            id = entry.id
            title = entry.title
            description = entry.description
            publish_date = parser.parse(entry.published)
            cover_image = entry.media_thumbnail[0]["url"]
            link = entry.link

            news = News(
                article_id=id,
                title=title,
                description=description,
                publish_date=publish_date,
                cover_image=cover_image,
                link=link,
            )
            self.store_in_db(news=news)
            print(news.id)
            break
