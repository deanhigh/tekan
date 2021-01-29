import math
from functools import partial, reduce

import matplotlib.pyplot as plt
import pandas as pd
from conf import MONGO
from mdl import DATE, ADJ_CLOSE, HIGH, LOW, CLOSE, VOLUME, OPEN
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


class Smoothing(object):
    """ class containing some smoothing functions used in some of the indicator """

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


class Indicator(object):
    ticker_source = None

    @classmethod
    def create(cls, ticker_source, *args, **kwargs):
        m = cls(*args, **kwargs)
        m.ticker_source = ticker_source
        return m

    def calc(self, *args, **kwargs):
        raise NotImplementedError('{} has not implemented calc method'.format(self))


class SMA(Indicator):
    """ Simple moving average on a field of choice"""

    def calc(self, period=20, field=ADJ_CLOSE):
        return self.ticker_source.underlying_field_df(field).rolling(period).mean().rename(
            columns={field: 'MA{}'.format(period)})


class STDDEV(Indicator):
    """Standard deviation of a field"""

    def calc(self, period=20, field=ADJ_CLOSE):
        return self.ticker_source.underlying_field_df(field).rolling(period).std().rename(
            columns={field: 'STDDEV{}'.format(period)})


class TR(Indicator):
    """ True range """

    def _tr(self, vals):
        prev_close = vals[CLOSE + '_prev']
        m1 = (vals[HIGH] - vals[LOW])
        m2 = abs(vals[HIGH] - prev_close)
        m3 = abs(vals[LOW] - prev_close)
        tr = max(m1, m2, m3) if not math.isnan(prev_close) else None
        return tr

    def calc(self):
        data = self.ticker_source.underlying_field_df(HIGH). \
            join(self.ticker_source.underlying_field_df(LOW)). \
            join(self.ticker_source.underlying_field_df(CLOSE)). \
            join(self.ticker_source.underlying_field_df(CLOSE).shift(), rsuffix='_prev')
        tr = data.apply(self._tr, axis=1).to_frame(name='TR')
        return tr


class ATR(Indicator):
    """ Average True Range """

    def calc(self, period=14):
        atr = TR.create(self.ticker_source).calc().rolling(period).apply(Smoothing.smoothing(period)).rename(
            columns={'TR': 'ATR{}'.format(period)})
        return atr


class ATRP(Indicator):
    """Average true range as percentage of close"""

    def calc(self, period=14):
        data = ATR.create(self.ticker_source).calc(period).join(self.ticker_source.underlying_field_df(CLOSE))
        return data.apply(lambda v: (v['ATR{}'.format(period)] / v[CLOSE]) * 100, axis=1).to_frame(
            'ATRP{}'.format(period))


class DM(Indicator):
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

    def calc(self):
        data = self._combine_data()

        return data.apply(self._dmp, axis=1).to_frame(name='+DM') \
            .join(data.apply(self._dmn, axis=1).to_frame(name='-DM'))


class SmootherDM(Indicator):
    def __init__(self):
        self.previous = None

    def calc(self, period=14):
        dm = DM.create(self.ticker_source).calc()
        smtr = TR.create(self.ticker_source).calc().rolling(period).apply(Smoothing.first_smoothing(period)).rename(
            columns={'TR': 'TR{}'.format(period)})
        pdm = dm['+DM'].rolling(period).apply(Smoothing.first_smoothing(period)).to_frame('+DM{}'.format(period))
        ndm = dm['-DM'].rolling(period).apply(Smoothing.first_smoothing(period)).to_frame('-DM{}'.format(period))
        return smtr.join(pdm).join(ndm)


class DI(Indicator):
    """ Direction Indicator """

    def _dip(self, period, v):
        return 100 * (v['+DM{}'.format(period)] / v['TR{}'.format(period)])

    def _din(self, period, v):
        return 100 * (v['-DM{}'.format(period)] / v['TR{}'.format(period)])

    def calc(self, period=14):
        sdm = SmootherDM.create(self.ticker_source).calc(period)
        return sdm.apply(partial(self._dip, period), axis=1).to_frame(name='+DI{}'.format(period)).join(
            sdm.apply(partial(self._din, period), axis=1).to_frame(name='-DI{}'.format(period)))


class ADX(Indicator):
    """Average direction index"""

    def _didiff(self, period, v):
        return abs(v['+DI{}'.format(period)] - v['-DI{}'.format(period)])

    def _disum(self, period, v):
        return v['+DI{}'.format(period)] + v['-DI{}'.format(period)]

    def _dx(self, v):
        return 100 * (v['DIFF'] / v['SUM'])

    def calc(self, period=14):
        di = DI.create(self.ticker_source).calc(period)
        prep = di.apply(partial(self._didiff, period), axis=1).to_frame(name='DIFF').join(
            di.apply(partial(self._disum, period), axis=1).to_frame(name='SUM'))
        dx = prep.apply(self._dx, axis=1).to_frame(name='DX')
        return di.join(dx.join(
            dx.rolling(period).apply(Smoothing.smoothing(period)).rename(columns={'DX': 'ADX{}'.format(period)})))


class TypicalPrice(Indicator):
    """ The typical price is the average of High, Low & Close prices"""

    def _combine_data(self):
        return self.ticker_source.underlying_field_df(HIGH). \
            join(self.ticker_source.underlying_field_df(LOW)). \
            join(self.ticker_source.underlying_field_df(CLOSE))

    def calc(self):
        in_data = self._combine_data()
        return in_data.apply(lambda v: (v[HIGH] + v[LOW] + v[CLOSE]) / 3, axis=1).to_frame('TP')


class CCI(Indicator):
    """ See http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:commodity_channel_index_cci """

    def _cci(self, typical_prices, *args):
        period = args[0]
        constant = args[1]
        mean = sum(typical_prices) / period
        mean_deviation = reduce(lambda x, y: x + abs(mean - y), typical_prices, 0) / period
        cci = (typical_prices[-1] - mean) / (constant * mean_deviation)
        return cci

    def calc(self, period=20, constant=0.015):
        return TypicalPrice.create(self.ticker_source).calc(). \
            rolling(period).apply(self._cci,
                                  args=(period, constant)).rename(columns={'TP': 'CCI{}/{}'.format(period, constant)})


def get_all_indicators_df(ticker_source):
    ind = [STDDEV, SMA, ATR, ATRP, ADX, CCI]
    return reduce(lambda df, ndf: df.join(ndf.create(ticker_source).calc()), ind, ticker_source.underlying_df())


if __name__ == '__main__':
    plt.style.use('dark_background')
