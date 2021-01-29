from ta.mdl import DataSet, IndicatorSeriesPointer


class IndicatorDataSetWrapper(DataSet):
    def __init__(self, id, indicator):
        super(IndicatorDataSetWrapper, self).__init__(id)
        self.indicator = indicator

    def load(self):
        self.data_frame = self.indicator.calc().data_frame

class Indicator(object):
    def __init__(self, id):
        self.id = id if id else str(self)

    def calc(self, context):
        raise NotImplementedError('{} has not implemented calc method'.format(self))

    def output_pointers(self):
        return {self.id: IndicatorSeriesPointer(self, self.id)}

    def __str__(self):
        return self.id
