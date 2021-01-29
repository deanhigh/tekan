import os
import unittest

# from mongoengine.connection import disconnect, connect
from pprint import pprint

import mongomock
from pandas import DataFrame
from pandas.util.testing import assert_frame_equal, assert_series_equal, assert_index_equal
from ta.data_management import FileSource
from ta.data_management.mongo_ds import DataFrameMongoWriter, MongoTimeSeriesSource
from ta.db import DATE, OPEN, CLOSE, VOLUME
from ta.db.mongo_tools import TS_DB


class TestMongoDataSource(unittest.TestCase):

    def setUp(self):
        # disconnect(TS_DB)
        # connect(TS_DB, host='mongomock://localhost', alias=TS_DB)
        self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))

    # def tearDown(self):
    #     disconnect(TS_DB)

    def test_read_write_dataframe_to_mongo(self):

        collection_mock = mongomock.MongoClient().db.collection
        collection_mock.ensure_index(DATE, unique=True)

        # Write data to collection
        DataFrameMongoWriter(collection_mock).write(self.ds.data_frame)
        # Read data from collection
        mtss = MongoTimeSeriesSource('TEST', collection_mock)

        assert_index_equal(self.ds.data_frame.index, mtss.data_frame.index)
        assert_series_equal(self.ds.data_frame[OPEN], mtss.data_frame[OPEN])
        assert_series_equal(self.ds.data_frame[CLOSE], mtss.data_frame[CLOSE])
        # Should not change the datatype
        #assert_series_equal(self.ds.data_frame[VOLUME], mtss.data_frame[VOLUME])