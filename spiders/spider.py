import time
from utils.constants import config as config_file

class Spider:
    def __init__(self) -> None:
        self.config = config_file
        self.check_updates()

    def parse(self):
        """
        This function parses the rss feed
        """
        raise NotImplementedError

    def check_updates(self):
        """
        This function re-run the spider after a specific period of time
        """

        sleep_time = self.config.spider_sleep_time

        while True:
            self.parse()
            time.sleep(sleep_time)
