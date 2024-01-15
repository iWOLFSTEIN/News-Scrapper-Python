import feedparser
from utils.constants import config


class FoxNewsSpider:
    def __init__(self) -> None:
        self.parse_and_notify()

    def parse_and_notify(self):
        feed = feedparser.parse(config.feed_urls.fox_news)
        for entry in feed.entries:
            print(entry)
            break
