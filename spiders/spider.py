import feedparser
import traceback
from models.news import News
from database.mongodb_client import MongoDBClient
import asyncio
from database.local_db import LocalDB
from utils.constants import config
from dateutil import parser
import hashlib


class Spider:
    def __init__(self, url, db_key, source_name) -> None:
        self.url = url
        self.db_key = db_key
        self.source_name = source_name
        self.mongodb_client = MongoDBClient(config.mongodb.name, config.mongodb.uri)
        self.collection_name = config.mongodb.collections[0]
        self.loop = asyncio.get_event_loop()
        self.parse()

    def extract_data(self, entry, id) -> News:
        news = News(
            id=id,
            title=entry.title,
            description=entry.description,
            publish_date=parser.parse(entry.published),
            cover_image=entry.media_thumbnail[0]["url"],
            link=entry.link,
            source_name=self.source_name,
        )

        return news

    def generate_sha256_hash(self, input_string):
        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_string.encode("utf-8"))
        hash_result = sha256_hash.hexdigest()
        return hash_result[:24]

    def parse(self):
        """
        This function parses the rss feed
        """
        try:
            feed = feedparser.parse(self.url)
            count = 0
            for entry in feed.entries:
                id = self.generate_sha256_hash(entry.id)
                if not self.is_rss_feed_updated(self.db_key, id, count):
                    break

                news = self.extract_data(entry, id)

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
            self.mongodb_client.insert_document(
                self.collection_name, news.model_dump(by_alias=True)
            )
        )

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

    def __del__(self):
        self.mongodb_client.close()
