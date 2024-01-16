import feedparser
from utils.constants import config


class FoxNewsSpider:
    def __init__(self) -> None:
        self.parse_and_notify()

    def parse_and_notify(self):
        feed = feedparser.parse(config.rss_feeds.fox_news.url)
        for entry in feed.entries:
            print(entry)
            break
