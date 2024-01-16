from spiders.fox_news import FoxNewsSpider
from spiders.life_hacker import LifeHackerSpider
from database.mongodb_client import MongoDBClient
from utils.constants import config


mongodb = MongoDBClient(config.mongodb.name, config.mongodb.uri)
# lhs = LifeHackerSpider()
fns = FoxNewsSpider()
