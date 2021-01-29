from sources import MongoTickerSource


class TestTickerSource(MongoTickerSource):
    def __init__(self, ticker):
        super().__init__(ticker)