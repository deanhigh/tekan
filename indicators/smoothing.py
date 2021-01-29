from functools import partial


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
