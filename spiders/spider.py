import time
from models.news import News
from utils.constants import config as config_file
from database.mongodb_client import MongoDBClient
import asyncio
from database.local_db import LocalDB


class Spider:
    def __init__(self) -> None:
        self.config = config_file
        self.mongodb_client = MongoDBClient(
            self.config.mongodb.name, self.config.mongodb.uri
        )
        self.collection_name = self.config.mongodb.collections[0]
        self.loop = asyncio.get_event_loop()
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

        self.loop.run_until_complete(
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

    def is_rss_feed_updated(self, key, value):
        """
        This method compares the top news id of previous rss feed to the top news id of current one to check if there's some change
        """

        retrieved_value = LocalDB.retrieve_data(key)

        if retrieved_value == value:
            return False
        elif retrieved_value is None:
            LocalDB.write_data(key, value)

        return True
