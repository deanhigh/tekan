from ta.indicators import Indicator, talib, Series


class TR(Indicator):
    def __init__(self, id, low_data_id, high_data_id, close_data_id):
        self.low_data_id = low_data_id
        self.high_data_id = high_data_id
        self.close_data_id = close_data_id
        super(TR, self).__init__(id)

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['low_data_id'], kwargs['high_data_id'], kwargs['close_data_id'])

    def calc(self, context):
        low_series = context.get_data(self.low_data_id)
        high_series = context.get_data(self.high_data_id)
        close_series = context.get_data(self.close_data_id)
        return Series(talib.TRANGE(high_series.values, low_series.values, close_series.values),
                      index=low_series.index.values)


class ATR(TR):
    def __init__(self, id, low_data_id, high_data_id, close_data_id, period):
        self.period = period
        super(ATR, self).__init__(id, low_data_id, high_data_id, close_data_id)

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['low_data_id'], kwargs['high_data_id'], kwargs['close_data_id'],
                   kwargs['period'])

    def calc(self, context):
        low_series = context.get_data(self.low_data_id)
        high_series = context.get_data(self.high_data_id)
        close_series = context.get_data(self.close_data_id)
        return Series(talib.ATR(high_series.values, low_series.values, close_series.values, self.period),
                      index=low_series.index.values)


class NATR(ATR):
    """True range as a percentage of close """
    def calc(self, context):
        low_series = context.get_data(self.low_data_id)
        high_series = context.get_data(self.high_data_id)
        close_series = context.get_data(self.close_data_id)
        return Series(talib.NATR(high_series.values, low_series.values, close_series.values, self.period),
                      index=low_series.index.values)
