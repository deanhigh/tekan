import logging
from sources import MongoTickerSource

logging.basicConfig(level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


class TestTickerSource(MongoTickerSource):
    def __init__(self, ticker):
        super().__init__(ticker)