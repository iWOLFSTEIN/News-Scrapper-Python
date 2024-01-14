from feed_sites import FOX_SPORTS_ALL_HEADLINES
import feedparser


class FoxNewsSpider:
    def __init__(self) -> None:
        feed = feedparser.parse(FOX_SPORTS_ALL_HEADLINES)
        print(feed)
