import pandas
from pandas import DataFrame, read_csv

from ta.mdl import DataFrameDataSet, ExportableDataFrameDataSet



class FileSource(DataFrameDataSet, ExportableDataFrameDataSet):
    def __init__(self, id, filename, fields=None):
        super(FileSource, self).__init__(id, fields)
        self.fields = fields
        self.filename = filename

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['filename'], kwargs.get('fields'))

    def load(self):
        if self.fields:
            self.data_frame = read_csv(self.filename, index_col=0, parse_dates=True).rename(columns=self.fields)
        else:
            self.data_frame = read_csv(self.filename, index_col=0, parse_dates=True)
