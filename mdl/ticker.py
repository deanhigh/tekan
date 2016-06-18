from datasources.yahoo.yfds import TickerDataRetriever


class Ticker(object):
    def __init__(self, symbol):
        self.symbol = symbol
        self.yds = TickerDataRetriever(symbol)

    def get_ts(self, data_type, range):
        return self.yds.get_ts_data(data_type, range)

    def __str__(self):
        return self.symbol
