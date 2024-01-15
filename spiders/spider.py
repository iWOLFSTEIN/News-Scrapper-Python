import time
from models.news import News
from utils.constants import config as config_file
from database.mongodb_client import MongoDBClient
import asyncio


class Spider:
    def __init__(self) -> None:
        self.config = config_file
        self.mongodb_client = MongoDBClient(
            self.config.mongodb.name, self.config.mongodb.uri
        )
        self.collection_name = self.config.mongodb.collections[0]
        self.check_updates()

    def parse(self):
        """
        This function parses the rss feed
        """
        raise NotImplementedError

    def store_in_db(self, news: News):
        """
        This function is used to store the scrapped news in the database
        """

        asyncio.run(
            self.mongodb_client.insert_document(self.collection_name, news.dict())
        )

    def check_updates(self):
        """
        This function re-run the spider after a specific period of time
        """

        sleep_time = self.config.spider_sleep_time
        seconds_in_hour = 3600

        while True:
            self.parse()
            self.mongodb_client.close()
            time.sleep(sleep_time * seconds_in_hour)
