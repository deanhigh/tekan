import datetime
import unittest

from pandas import DataFrame

from ta.connectors.yahoo import YahooDataSource


class MockLocalStore(object):

    def __init__(self, id, range_start, range_end):
        self.id = id
        self.range_start = range_start
        self.range_end = range_end
        self.data_frame = DataFrame()

    def load(self):
        pass

    def is_complete(self):
        if len(self.data_frame) == 0: return False
        else:
            print(self.data_frame.index.max(), self.range_end)
            return self.data_frame.index.max() >= self.range_end


    def write(self, df):
        self.data_frame = df

    @classmethod
    def create(cls, id, range_start, range_end ):
        return cls(id, range_start, range_end)

class YahooIntegrationTest(unittest.TestCase):
    def test_fetch_data(self):
        ds = YahooDataSource("AAPL")
        self.assertGreater(len(ds.data_frame),0)

    def test_local_store(self):
        ds = YahooDataSource("AAPL", datetime.datetime.strptime('2017-02-06', '%Y-%m-%d'), datetime.datetime.strptime('2017-02-08', '%Y-%m-%d'), local_store_factory=MockLocalStore.create)
        self.assertEqual(len(ds.data_frame), 3)
        self.assertTrue(ds.local_store.is_complete())
        ds.range_end = ds.local_store.range_end = datetime.datetime.strptime('2017-02-09', '%Y-%m-%d')
        self.assertFalse(ds.local_store.is_complete())
        ds.load()
        self.assertTrue(ds.local_store.is_complete())
        self.assertEqual(len(ds.data_frame), 4)


if __name__ == '__main__':
    unittest.main()
