from yahoo_finance import Share


class TickerDataRetriever(object):
    def __init__(self, ticker):
        self.share = Share(ticker)
        #self.data_type_retrievers = {HIGH: self.ts_historical}

    def get_ts_data(self, data_type, date_range):
        _data = self.share.get_historical(*date_range)
        # dt_ds = self.data_type_retrievers.get(data_type)
        return _data if _data else None

    def ts_historical(self, date_range):
        return self.share.get_historical(*date_range)
