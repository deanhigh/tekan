import matplotlib.pyplot as plt
import pandas as pd
from conf import MONGO
from mdl import DATE, ADJ_CLOSE, HIGH, LOW, CLOSE, VOLUME, OPEN
from numpy.core.numeric import ndarray
from pymongo import MongoClient

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


class Measure(object):
    ticker_source = None

    @classmethod
    def create(cls, ticker_source, *args, **kwargs):
        m = cls(*args, **kwargs)
        m.ticker_source = ticker_source
        return m


class MA(Measure):
    def ma(self, period=20, field=ADJ_CLOSE):
        return self.ticker_source.underlying_field_df(field).rolling(period).mean().rename(
            columns={field: 'MA{}'.format(period)})


class STDDEV(Measure):
    def std(self, period=20, field=ADJ_CLOSE):
        return self.ticker_source.underlying_field_df(field).rolling(period).std().rename(
            columns={field: 'STD{}'.format(period)})


class TR(Measure):
    def _tr(self, vals):
        prev_close = vals[CLOSE + '_prev']
        m1 = (vals[HIGH] - vals[LOW])
        m2 = abs(vals[HIGH] - prev_close) if prev_close else -1
        m3 = abs(vals[LOW] - prev_close) if prev_close else -1
        tr = max(m1, m2, m3)
        return tr

    def tr(self):
        data = self.ticker_source.underlying_field_df(HIGH). \
            join(self.ticker_source.underlying_field_df(LOW)). \
            join(self.ticker_source.underlying_field_df(CLOSE)). \
            join(self.ticker_source.underlying_field_df(CLOSE).shift(), rsuffix='_prev')
        tr = data.apply(self._tr, axis=1)
        print(tr)
        return tr


class ATR(TR):
    def atr(self, period=14):
        atr = self.tr().rolling(period).mean()
        print(atr)
        return atr


def plot_samples():
    with MongoTickerSource('ADBE') as ts:
        df = ts.underlying_field_df().join(ts.underlying_field_df(HIGH)).join(ts.underlying_field_df(LOW)).join(
            ts.underlying_field_df(ADJ_CLOSE)). \
            join(TR.create(ts).tr()).join(ATR.atr())
        df.to_csv('ADBE')


if __name__ == '__main__':
    plt.style.use('dark_background')
    plot_samples()
