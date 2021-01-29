from conf import MONGO
from mdl import HIGH, LOW, OPEN, CLOSE, ADJ_CLOSE, VOLUME, DATE
from pymongo import MongoClient
import pandas as pd


MONGO_DATABASE_NAME = 'quotes'


class TickerSource(object):
    def underlying_field_df(self, field=ADJ_CLOSE):
        pass

    def underlying_df(self):
        pass


class MongoTickerSource(TickerSource):
    def __init__(self, ticker):
        super(MongoTickerSource, self).__init__()
        self.ticker = ticker
        self.data = None

    def __enter__(self):
        self.mc = MongoClient(*MONGO)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mc.close()

    def exists(self):
        return self.ticker in self.mc.get_database(MONGO_DATABASE_NAME).collection_names()

    def all_data(self, col):
        if not self.data:
            self.data = [x for x in self.mc.get_database(MONGO_DATABASE_NAME).get_collection(col).find()]
            self.index = pd.DatetimeIndex([i[DATE] for i in self.data])
        return self.data

    def underlying_field_df(self, field=ADJ_CLOSE):
        col = self.all_data(self.ticker)
        return pd.DataFrame(
            data={field: list(map(lambda x: x[field], col))},
            index=self.index,
            dtype=float).sort_index()

    def underlying_df(self, fields=(HIGH, LOW, OPEN, CLOSE, ADJ_CLOSE, VOLUME)):
        col = self.all_data(self.ticker)
        data = {x: [] for x in fields}
        for i in col:
            for f in fields:
                data[f].append(i[f])

        return pd.DataFrame(
            data=data,
            index=self.index,
            dtype=float).sort_index()
