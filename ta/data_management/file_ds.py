import pandas
from pandas import DataFrame, read_csv

from conf import get_full_data_path
from ta.mdl import DataFrameDataSet, Writer


class CsvFileWriter(Writer):

    def __init__(self, filename):
        self.filename = filename

    def write(self, data_frame):
        data_frame.to_csv(self.filename)


class FileSource(DataFrameDataSet):
    def __init__(self, id, filename, fields=None):
        super(FileSource, self).__init__(id, fields)
        self.fields = fields
        self.filename = filename

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['filename'], kwargs.get('fields'))

    def load(self):
        if self.fields:
            self.data_frame = read_csv(get_full_data_path(self.filename), index_col=0, parse_dates=True).rename(columns=self.fields)
        else:
            self.data_frame = read_csv(get_full_data_path(self.filename), index_col=0, parse_dates=True)
