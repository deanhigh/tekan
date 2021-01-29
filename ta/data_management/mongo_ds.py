from pprint import pprint

from ta.mdl import DataFrameDataSet, Writer


class MongoTimeSeriesSource(DataFrameDataSet):
    def __init__(self, id, collection=None, fields=None):
        super(MongoTimeSeriesSource, self).__init__(id, fields)
        self.fields = fields
        self.collection = collection

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['filename'], kwargs.get('fields'))

    def load(self):
        pass
        # if self.fields:
        #     self.data_frame = read_csv(get_full_data_path(self.filename), index_col=0, parse_dates=True).rename(columns=self.fields)
        # else:
        #     self.data_frame = read_csv(get_full_data_path(self.filename), index_col=0, parse_dates=True)


class MongoWriter(Writer):

    def write(self, data_frame):
        pprint(data_frame.to_dict())