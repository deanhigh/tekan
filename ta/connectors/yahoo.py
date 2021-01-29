import datetime as datetime

from pandas_datareader import data

from conf import MONGO
from ta.mdl import DataFrameDataSet


class YahooDataSource(DataFrameDataSet):

    def __init__(self, id, range_start=None, range_end=None, series_ids=None, local_store_factory=None):
        super(YahooDataSource, self).__init__(id, series_ids)
        self.range_start = range_start if range_start else datetime.datetime.today() - datetime.timedelta(days=5)
        self.range_end = range_end if range_end else datetime.date.today()
        self.local_store = None if not local_store_factory else local_store_factory(id, range_start, range_end)

    def load(self):
        if self.local_store:
            self.local_store.load()
            if self.local_store.is_complete():
                self.data_frame = self.local_store.data_frame
            else:
                self.data_frame = data.DataReader(self.id, 'yahoo', self.range_start, self.range_end)
                self.local_store.write(self.data_frame)
        else:
            self.data_frame = data.DataReader(self.id, 'yahoo', self.range_start, self.range_end)

    def __str__(self):
        return self.id
