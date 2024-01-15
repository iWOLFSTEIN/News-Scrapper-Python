import yaml
import time


class Spider:
    def __init__(self) -> None:
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

        config = yaml.safe_load(open("config.yaml"))
        sleep_time = config["SPIDER_SLEEP_TIME"]

        while True:
            self.parse()
            time.sleep(sleep_time)
