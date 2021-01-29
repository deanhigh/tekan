import unittest

from ta.connectors.yahoo import YahooDataSource


class YahooIntegrationTest(unittest.TestCase):
    def test_fetch_data(self):
        ds = YahooDataSource("AAPL")
        self.assertGreater(len(ds.data_frame),0)


if __name__ == '__main__':
    unittest.main()
