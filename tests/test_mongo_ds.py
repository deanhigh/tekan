import os
import unittest

from mongoengine.connection import disconnect, connect

from ta.data_management import FileSource
from ta.data_management.mongo_ds import MongoWriter
from ta.db.mongo_tools import TS_DB


class TestMongoDataSource(unittest.TestCase):

    def setUp(self):
        disconnect(TS_DB)
        connect(TS_DB, host='mongomock://localhost', alias=TS_DB)
        self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))

        # //self.assertEqual([], mongo_tools.get_symbols())self

    def tearDown(self):
        disconnect(TS_DB)

    def test_write_to_mongo(self):
        MongoWriter().write(self.ds.data_frame)
        self.fail("Write to mongo store... AKA MongoWriter like CSV filewriter ")

    def test_read_from_store(self):
        self.fail("read from mongo into dataframe data set, use to_dict ")