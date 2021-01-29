from ta.mdl import Predicate


class CrossoverCondition(Predicate):
    def __init__(self, series_1, series_2):
        self.series_1 = series_1
        self.series_2 = series_2

    def apply(self, date):
        pass
