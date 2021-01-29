import talib
from pandas import Series

from ta.indicators.kpi import Indicator


class MovingAverage(Indicator):
    def __init__(self, id, input_data_id, period):
        self.input_data_id = input_data_id
        self.period = period
        super(MovingAverage, self).__init__(id)

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['input_data_id'], kwargs['period'])


class SMA(MovingAverage):
    """ Simple moving average on a field of choice"""

    def calc(self, context):
        source_series = context.get_data(self.input_data_id)
        return Series(data=talib.SMA(source_series.values, self.period), index=source_series.index.values)


class EMA(MovingAverage):
    """ Exponentially weighted moving average """

    def calc(self, context):
        source_series = context.get_data(self.input_data_id)
        return Series(data=talib.EMA(source_series.values, self.period), index=source_series.index.values)


class STDDEV(MovingAverage):
    """Standard deviation with rolling window"""

    def calc(self, context):
        source_series = context.get_data(self.input_data_id)
        return Series(talib.STDDEV(source_series.values, self.period), index=source_series.index.values)
