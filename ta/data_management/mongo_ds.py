from pprint import pprint

from pandas import DataFrame
from pymongo.collection import Collection

from ta.db import DATE
from ta.db.mongo_tools import get_source_ts_collection
from ta.mdl import DataFrameDataSet, Writer
import logging as log


class MongoTimeSeriesSource(DataFrameDataSet):
    def __init__(self, id, collection:Collection, fields=None):
        super(MongoTimeSeriesSource, self).__init__(id, fields)
        self.fields = fields
        self.collection = collection

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], get_source_ts_collection(kwargs['collection']), kwargs.get('fields'))

    def load(self):
        data = self.collection.find()
        self.data_frame = DataFrame.from_records(list(data), index=DATE).sort_index()
        # Rename the fields if fields is set
        if self.fields:
            self.data_frame = self.data_frame.rename(columns=self.fields)


class DataFrameMongoWriter(Writer):
    def __init__(self, collection: Collection):
        self.collection = collection

    def write(self, df: DataFrame):
        for ts, data in df.to_dict('index').items():
            data[DATE] = ts.to_datetime()
            if data[DATE]:
                log.debug(data)
                self.collection.insert_one(data)
            else:
                log.error('error, no date {}', data)
        # self.collection.insert_many()
