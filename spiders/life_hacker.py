from spiders.spider import Spider
from utils.constants import config


class LifeHackerSpider(Spider):
    def __init__(self) -> None:
        url = config.rss_feeds.life_hacker.url
        db_key = config.rss_feeds.life_hacker.local_db_key
        super().__init__(url, db_key)
