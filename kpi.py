import matplotlib.pyplot as plt
import pandas as pd
from conf import MONGO
from mdl import DATE, ADJ_CLOSE, HIGH, LOW, CLOSE
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
    #TODO : BUusy with this
    def _func(self, v):
        x = v[HIGH] - v[LOW]
        print(x)
        return v

    def tr(self):
        return self.ticker_source.ticker_df(HIGH).join(self.ticker_source.ticker_df(LOW)).join(
            self.ticker_source.ticker_df(CLOSE)).rolling(2).apply(self._func)

def plot_samples():
    with MongoTickerSource('ADBE') as ts:
        TR.create(ts).tr().plot()
        # ax = ts.ticker_df().plot()
        # ax = MA.create(ts).ma(50).plot(ax=ax)
        # ax = STDDEV.create(ts).std(10).plot(ax=ax)
        #
        plt.show()


if __name__ == '__main__':
    plt.style.use('dark_background')
    plot_samples()
