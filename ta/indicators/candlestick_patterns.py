from ta.indicators import Indicator, Series, talib
from ta.mdl.workflows import WorkflowContext


class Pattern(Indicator):
    def __init__(self, id, open, high, low, close):
        super(Pattern, self).__init__(id)
        self.close = close
        self.low = low
        self.high = high
        self.open = open

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['open_data_id'], kwargs['high_data_id'], kwargs['low_data_id'],
                   kwargs['close_data_id'])

    def get_params(self, context):
        h = context.get_data(self.high)
        l = context.get_data(self.low)
        o = context.get_data(self.open)
        c = context.get_data(self.close)
        return (o.values, h.values, l.values, c.values), o.index


class Doji(Pattern):

    def calc(self, context: WorkflowContext) -> Series:
        data, idx = self.get_params(context)
        return Series(talib.CDLDOJI(*data), index=idx)
