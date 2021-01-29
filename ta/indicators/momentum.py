from ta.indicators import Indicator, talib, Series


class DX(Indicator):
    def __init__(self, id, low_data_id, high_data_id, close_data_id, period):
        self.period = period
        self.low_data_id = low_data_id
        self.high_data_id = high_data_id
        self.close_data_id = close_data_id
        super(DX, self).__init__(id)

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['low_data_id'], kwargs['high_data_id'], kwargs['close_data_id'],
                   kwargs['period'])

    def calc(self, context):
        low_series = context.get_data(self.low_data_id)
        high_series = context.get_data(self.high_data_id)
        close_series = context.get_data(self.close_data_id)
        return Series(talib.DX(high_series.values, low_series.values, close_series.values, self.period),
                      index=low_series.index.values)



class ADX(DX):

    def calc(self, context):
        low_series = context.get_data(self.low_data_id)
        high_series = context.get_data(self.high_data_id)
        close_series = context.get_data(self.close_data_id)
        return Series(talib.ADX(high_series.values, low_series.values, close_series.values, self.period),
                      index=low_series.index.values)