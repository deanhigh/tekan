from functools import partial

import math

import matplotlib.pyplot as plt
import pandas as pd
from conf import MONGO
from mdl import DATE, ADJ_CLOSE, HIGH, LOW, CLOSE, VOLUME, OPEN
from pymongo import MongoClient
from logging import info

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
            columns={field: 'STDDEV{}'.format(period)})


class TR(Measure):
    def _tr(self, vals):
        prev_close = vals[CLOSE + '_prev']
        m1 = (vals[HIGH] - vals[LOW])
        m2 = abs(vals[HIGH] - prev_close)
        m3 = abs(vals[LOW] - prev_close)
        tr = max(m1, m2, m3) if not math.isnan(prev_close) else None
        return tr

    def tr(self):
        data = self.ticker_source.underlying_field_df(HIGH). \
            join(self.ticker_source.underlying_field_df(LOW)). \
            join(self.ticker_source.underlying_field_df(CLOSE)). \
            join(self.ticker_source.underlying_field_df(CLOSE).shift(), rsuffix='_prev')
        tr = data.apply(self._tr, axis=1).to_frame(name='TR')
        return tr


class Smoothing(object):
    def __init__(self):
        self.previous = None

    @classmethod
    def smoothing(cls, period):
        return partial(cls()._smoothing, period)

    def _smoothing(self, period, values):
        smoothed = (self.previous * (period - 1) + values[-1]) / period if self.previous else sum(values) / period
        self.previous = smoothed
        return self.previous

    @classmethod
    def first_smoothing(cls, period):
        return partial(cls()._first_smoothing, period)

    def _first_smoothing(self, period, vals):
        smoothed = self.previous - (self.previous / period) + vals[-1] if self.previous else sum(vals)
        self.previous = smoothed
        return smoothed


class ATR(TR):
    def atr(self, period=14):
        atr = self.tr().rolling(period).apply(Smoothing.smoothing(period)).rename(
            columns={'TR': 'ATR{}'.format(period)})
        return atr


class DM(Measure):
    def _dmp(self, v):
        prev_low = v[LOW + '_prev']
        prev_high = v[HIGH + '_prev']
        if not math.isnan(prev_low) and not math.isnan(prev_high):
            h = v[HIGH] - prev_high
            l = prev_low - v[LOW]
            return h if h > l and h > 0 else 0
        else:
            return None

    def _dmn(self, v):
        prev_low = v[LOW + '_prev']
        prev_high = v[HIGH + '_prev']
        if not math.isnan(prev_low) and not math.isnan(prev_high):
            l = prev_low - v[LOW]
            h = v[HIGH] - prev_high
            return l if l > h and l > 0 else 0
        else:
            return None

    def _combine_data(self):
        return self.ticker_source.underlying_field_df(HIGH). \
            join(self.ticker_source.underlying_field_df(LOW)). \
            join(self.ticker_source.underlying_field_df(HIGH).shift(), rsuffix='_prev'). \
            join(self.ticker_source.underlying_field_df(LOW).shift(), rsuffix='_prev')

    def dm(self):
        data = self._combine_data()

        return data.apply(self._dmp, axis=1).to_frame(name='+DM') \
            .join(data.apply(self._dmn, axis=1).to_frame(name='-DM'))


class SmootherDM(Measure):
    def __init__(self):
        self.previous = None

    def smoothed_dm(self, period=14):
        dm = DM.create(self.ticker_source).dm()
        smtr = TR.create(self.ticker_source).tr().rolling(period).apply(Smoothing.first_smoothing(period)).rename(
            columns={'TR': 'TR{}'.format(period)})
        pdm = dm['+DM'].rolling(period).apply(Smoothing.first_smoothing(period)).to_frame('+DM{}'.format(period))
        ndm = dm['-DM'].rolling(period).apply(Smoothing.first_smoothing(period)).to_frame('-DM{}'.format(period))
        return smtr.join(pdm).join(ndm)


class DI(Measure):
    def _dip(self, period, v):
        return 100 * (v['+DM{}'.format(period)] / v['TR{}'.format(period)])

    def _din(self, period, v):
        return 100 * (v['-DM{}'.format(period)] / v['TR{}'.format(period)])

    def di(self, period=14):
        sdm = SmootherDM.create(self.ticker_source).smoothed_dm(period)
        return sdm.apply(partial(self._dip, period), axis=1).to_frame(name='+DI{}'.format(period)).join(
            sdm.apply(partial(self._din, period), axis=1).to_frame(name='-DI{}'.format(period)))


class ADX(Measure):
    def _didiff(self, period, v):
        return abs(v['+DI{}'.format(period)] - v['-DI{}'.format(period)])

    def _disum(self, period, v):
        return v['+DI{}'.format(period)] + v['-DI{}'.format(period)]

    def _dx(self, v):
        return 100 * (v['DIFF'] / v['SUM'])

    def adx(self, period=14):
        di = DI.create(self.ticker_source).di(period)
        prep = di.apply(partial(self._didiff, period), axis=1).to_frame(name='DIFF').join(
            di.apply(partial(self._disum, period), axis=1).to_frame(name='SUM'))
        dx = prep.apply(self._dx, axis=1).to_frame(name='DX')
        return di.join(dx.join(dx.rolling(period).apply(Smoothing.smoothing(period)).rename(columns={'DX': 'ADX{}'.format(period)})))


def get_all_indicators_df(ticker_source):
        df = ticker_source.underlying_df()
        df = df.join(STDDEV.create(ticker_source).std())
        df = df.join(ATR.create(ticker_source).atr())
        df = df.join(ADX.create(ticker_source).adx())
        return df


#
# def plot_samples():
#     with MongoTickerSource('ADBE') as ts:
#         df = ts.underlying_field_df().join(ts.underlying_field_df(HIGH)).join(ts.underlying_field_df(LOW)).join(
#             ts.underlying_field_df(ADJ_CLOSE)). \
#             join(TR.create(ts).tr()).join(ATR.atr())
#         df.to_csv('ADBE')

if __name__ == '__main__':
    plt.style.use('dark_background')
