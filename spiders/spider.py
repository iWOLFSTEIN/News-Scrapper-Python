import feedparser
import time
import traceback
from models.news import News
from database.mongodb_client import MongoDBClient
import asyncio
from database.local_db import LocalDB
from utils.constants import config
from dateutil import parser


class Spider:
    def __init__(self, url, db_key) -> None:
        self.url = url
        self.db_key = db_key
        self.mongodb_client = MongoDBClient(config.mongodb.name, config.mongodb.uri)
        self.collection_name = config.mongodb.collections[0]
        self.loop = asyncio.get_event_loop()
        self.check_updates()

    def extract_data(self, entry) -> News:
        news = News(
            article_id=entry.id,
            title=entry.title,
            description=entry.description,
            publish_date=parser.parse(entry.published),
            cover_image=entry.media_thumbnail[0]["url"],
            link=entry.link,
        )

        return news

    def parse(self):
        """
        This function parses the rss feed
        """
        try:
            feed = feedparser.parse(self.url)
            count = 0
            for entry in feed.entries:
                if not self.is_rss_feed_updated(self.db_key, entry.id, count):
                    break

                news = self.extract_data(entry)

                self.store_in_db(news=news)
                count = count + 1
                if count == config.max_scrapped_news:
                    break

        except Exception as _:
            traceback.print_exc()

    def store_in_db(self, news: News):
        """
        This function is used to store the scrapped news in the database
        """

        self.loop.run_until_complete(
            self.mongodb_client.insert_document(self.collection_name, news.dict())
        )

    def check_updates(self):
        """
        This function re-run the spider after a specific period of time
        """

        sleep_time = config.spider_sleep_time
        seconds_in_hour = 3600

        while True:
            self.parse()
            self.mongodb_client.close()
            time.sleep(sleep_time * seconds_in_hour)

    def is_rss_feed_updated(self, key, value, count):
        """
        This method compares the top news id of previous rss feed to the top news id of current one to check if there's some change
        """

        retrieved_value = LocalDB.retrieve_data(key)

        if retrieved_value == value:
            return False
        elif retrieved_value is None or count == 0:
            LocalDB.write_data(key, value)

        return True
