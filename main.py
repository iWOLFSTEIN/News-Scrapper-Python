import time
from spiders.fox_news import FoxNewsSpider
from spiders.life_hacker import LifeHackerSpider
from utils.constants import config


def main():
    while True:
        FoxNewsSpider()
        LifeHackerSpider()
        time.sleep(config.spider_sleep_time * 3600)


if __name__ == "__main__":
    main()
