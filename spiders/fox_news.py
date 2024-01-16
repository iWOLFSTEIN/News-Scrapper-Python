from spiders.spider import Spider
from utils.constants import config


class FoxNewsSpider(Spider):
    def __init__(self) -> None:
        url = config.rss_feeds.fox_news.url
        db_key = config.rss_feeds.fox_news.local_db_key
        source_name = config.rss_feeds.fox_news.name
        super().__init__(url, db_key, source_name)
