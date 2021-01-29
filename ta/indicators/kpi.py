import math
from functools import partial, reduce

import numpy as np
import talib

from ta.db import ADJ_CLOSE, HIGH, LOW, CLOSE
from ta.indicators.smoothing import Smoothing


class Indicator(object):

    def __init__(self, input_data_set):
        self.input_data_set = input_data_set

    def calc(self):
        raise NotImplementedError('{} has not implemented calc method'.format(self))



class MovingAverage(Indicator):
    def __init__(self, input_data_set, period, field):
        super(MovingAverage, self).__init__(input_data_set)
        self.period = period
        self.field = field


class SMA(MovingAverage):
    """ Simple moving average on a field of choice"""

    def calc(self):
        self.input_data_set.data_frame['MA{}'.format(self.period)] = talib.SMA(self.input_data_set.data_frame[self.field].values, self.period)
        return self.input_data_set


class EMA(MovingAverage):
    """ Exponentially weighted moving average """

    def calc(self):
        self.input_data_set.data_frame['EMA{}'.format(self.period)] = talib.EMA(self.input_data_set.data_frame[ADJ_CLOSE].values, self.period)
        return self.input_data_set


class STDDEV(Indicator):
    """Standard deviation of a field"""

    def calc(self, period=20, field=ADJ_CLOSE):
        return self.input_data_set.underlying_field_df(field).rolling(period).std().rename(
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
        data = self.input_data_set.underlying_field_df(HIGH). \
            join(self.input_data_set.underlying_field_df(LOW)). \
            join(self.input_data_set.underlying_field_df(CLOSE)). \
            join(self.input_data_set.underlying_field_df(CLOSE).shift(), rsuffix='_prev')
        tr = data.apply(self._tr, axis=1).to_frame(name='TR')
        return tr


class ATR(Indicator):
    """ Average True Range """

    def calc(self, period=14):
        atr = TR.create(self.input_data_set).calc().rolling(period).apply(Smoothing.smoothing(period)).rename(
            columns={'TR': 'ATR{}'.format(period)})
        return atr


class ATRP(Indicator):
    """Average true range as percentage of close"""

    def calc(self, period=14):
        data = ATR.create(self.input_data_set).calc(period).join(self.input_data_set.underlying_field_df(CLOSE))
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
        return self.input_data_set.underlying_field_df(HIGH). \
            join(self.input_data_set.underlying_field_df(LOW)). \
            join(self.input_data_set.underlying_field_df(HIGH).shift(), rsuffix='_prev'). \
            join(self.input_data_set.underlying_field_df(LOW).shift(), rsuffix='_prev')

    def calc(self):
        data = self._combine_data()

        return data.apply(self._dmp, axis=1).to_frame(name='+DM') \
            .join(data.apply(self._dmn, axis=1).to_frame(name='-DM'))


class SmootherDM(Indicator):
    def __init__(self):
        self.previous = None

    def calc(self, period=14):
        dm = DM.create(self.input_data_set).calc()
        smtr = TR.create(self.input_data_set).calc().rolling(period).apply(Smoothing.first_smoothing(period)).rename(
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
        sdm = SmootherDM.create(self.input_data_set).calc(period)
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
        di = DI.create(self.input_data_set).calc(period)
        prep = di.apply(partial(self._didiff, period), axis=1).to_frame(name='DIFF').join(
            di.apply(partial(self._disum, period), axis=1).to_frame(name='SUM'))
        dx = prep.apply(self._dx, axis=1).to_frame(name='DX')
        return di.join(dx.join(
            dx.rolling(period).apply(Smoothing.smoothing(period)).rename(columns={'DX': 'ADX{}'.format(period)})))


class TypicalPrice(Indicator):
    """ The typical price is the average of High, Low & Close prices"""

    def _combine_data(self):
        return self.input_data_set.underlying_field_df(HIGH). \
            join(self.input_data_set.underlying_field_df(LOW)). \
            join(self.input_data_set.underlying_field_df(CLOSE))

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
        return TypicalPrice.create(self.input_data_set).calc(). \
            rolling(period).apply(self._cci,
                                  args=(period, constant)).rename(columns={'TP': 'CCI{}/{}'.format(period, constant)})


class MarketVolatilityType(Indicator):
    def _run(self, v):
        d3 = (v[2] - v[1]) / 3
        val = v[0]

        return 0 if val < v[1] + d3 else 1 if val < v[2] - d3 else 2

    def calc(self, period=20):
        df = ATR.create(self.input_data_set).calc(period=period)
        df_minmax = df.rolling(period).agg([np.min, np.max])
        df_mvt = df.join(df_minmax).apply(self._run, axis=1).to_frame(name='MVT')
        return df.join(df_minmax.join(df_mvt))
