from ta.mdl import Predicate
from ta.mdl.workflows import WorkflowContext


class CrossOver(Predicate):
    """
    Does series 1 cross over series 2 at a given date
    """
    def __init__(self, series_1, series_2):
        self.series_1 = series_1
        self.series_2 = series_2

    def apply(self, date):
        previous_1 = self.series_1.data.shift(1)
        previous_2 = self.series_2.data.shift(1)
        return ((self.series_1.data >= self.series_2.data) & (previous_1 <= previous_2))[date]


class CrossUnder(CrossOver):
    """
    Does series 1 cross under series 2 at a given date
    """

    def __init__(self, series_1, series_2):
        super(CrossUnder, self).__init__(series_2, series_1)  # reverse the order