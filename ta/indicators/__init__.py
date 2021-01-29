from ta.mdl import DataSet


class IndicatorDataSetWrapper(DataSet):
    def __init__(self, id, indicator):
        super(IndicatorDataSetWrapper, self).__init__(id)
        self.indicator = indicator

    def load(self):
        self.data_frame = self.indicator.calc().data_frame
