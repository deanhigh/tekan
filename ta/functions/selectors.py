from ta.mdl import Function
import logging

log = logging.getLogger("selectors")

class TimeSeriesSelector(Function):
    def __init__(self, id, ts_input, date_idx):
        super(TimeSeriesSelector, self).__init__(id)
        self.ts_input = ts_input
        self.date_idx = date_idx

    def apply(self, context):
        log.debug("Select %s from %s", self.date_idx, self.ts_input)
        return context.get_data(self.ts_input)[self.date_idx]

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['ts_input'], kwargs['date_idx'])

