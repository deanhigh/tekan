import matplotlib.pyplot as plt
import pandas as pd
from conf import MONGO
from mdl import DATE, ADJ_CLOSE, HIGH, LOW, CLOSE
from numpy.core.numeric import ndarray
from pymongo import MongoClient

MONGO_DATABASE_NAME = 'quotes'


class TickerSource(object):
    def ticker_df(self):
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

    def _all_data(self, col):
        if not self.data:
            self.data = [x for x in self.mc.get_database(MONGO_DATABASE_NAME).get_collection(col).find()]
            self.index = pd.DatetimeIndex([i[DATE] for i in self.data])
        return self.data

    def ticker_df(self, field=ADJ_CLOSE):
        col = self._all_data(self.ticker)
        return pd.DataFrame(
            data={field: list(map(lambda x: x[field], col))},
            index=self.index,
            dtype=float)


class Measure(object):
    ticker_source = None

    @classmethod
    def create(cls, ticker_source, *args, **kwargs):
        m = cls(*args, **kwargs)
        m.ticker_source = ticker_source
        return m


class MA(Measure):
    def ma(self, period=20, field=ADJ_CLOSE):
        return self.ticker_source.ticker_df(field).rolling(period).mean().rename(columns={field: 'MA{}'.format(period)})


class STDDEV(Measure):
    def std(self, period=20, field=ADJ_CLOSE):
        return self.ticker_source.ticker_df(field).rolling(period).std().rename(columns={field: 'STD{}'.format(period)})


class TR(Measure):
    def _tr(self, vals):
        prev_close = vals[CLOSE + '_prev']
        m1 = (vals[HIGH] - vals[LOW])
        m2 = abs(vals[HIGH] - prev_close) if prev_close else -1
        m3 = abs(vals[LOW] - prev_close) if prev_close else -1
        tr = max(m1, m2, m3)
        return tr

    def tr(self):
        data = self.ticker_source.ticker_df(HIGH). \
            join(self.ticker_source.ticker_df(LOW)). \
            join(self.ticker_source.ticker_df(CLOSE)). \
            join(self.ticker_source.ticker_df(CLOSE).shift(), rsuffix='_prev')
        return data.apply(self._tr, axis=1)


class ATR(TR):
    def atr(self, period=14):
        return self.tr().rolling(period).mean()


def plot_samples():
    with MongoTickerSource('ADBE') as ts:
        ax = ts.ticker_df().plot()
        # ax = MA.create(ts).ma(50).plot(ax=ax)
        ax = ATR.create(ts).atr().plot(ax=ax)
        # ax = STDDEV.create(ts).std(10).plot(ax=ax)
        #
        plt.show()


if __name__ == '__main__':
    plt.style.use('dark_background')
    plot_samples()
