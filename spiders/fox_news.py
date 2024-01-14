from utils.feed_sites import FOX_SPORTS_ALL_HEADLINES
import feedparser


class FoxNewsSpider:
    def __init__(self) -> None:
        self.parse_and_notify()

    def parse_and_notify(self):
        feed = feedparser.parse(FOX_SPORTS_ALL_HEADLINES)
        for entry in feed.entries:
            print(entry)
            break
