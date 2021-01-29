import unittest

from ta.connectors.yahoo import YahooDataSource


class YahooIntegrationTest(unittest.TestCase):
    def test_fetch_data(self):
        ds = YahooDataSource("AAPL")
        self.assertEqual(1, len(ds.data_frame))


if __name__ == '__main__':
    unittest.main()
