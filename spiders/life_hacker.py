import traceback
from spiders.spider import Spider
import feedparser
from dateutil import parser
from models.news import News


class LifeHackerSpider(Spider):
    def parse(self):
        try:
            max_allowed_to_scrap = self.config.max_scrapped_news
            feed = feedparser.parse(self.config.rss_feeds.life_hacker.url)
            for entry in feed.entries:
                if not self.is_rss_feed_updated(
                    self.config.rss_feeds.life_hacker.local_db_key, entry.id
                ):
                    break

                news = News(
                    article_id=entry.id,
                    title=entry.title,
                    description=entry.description,
                    publish_date=parser.parse(entry.published),
                    cover_image=entry.media_thumbnail[0]["url"],
                    link=entry.link,
                )

                self.store_in_db(news=news)
                max_allowed_to_scrap = max_allowed_to_scrap - 1
                if max_allowed_to_scrap == 0:
                    break

        except Exception as _:
            traceback.print_exc()
