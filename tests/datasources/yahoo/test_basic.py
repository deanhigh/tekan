import unittest

from connectors.yahoo.yfds import TickerDataRetriever
from ddt import ddt, data

tickers = ['PNRG', 'LIT', 'ADBE']

@ddt
class TestTickers(unittest.TestCase):
    @data(*tickers)
    def test_yahoo_data_fetcher(self, ticker):
        tdr = TickerDataRetriever('ADBE')
        print(tdr.share.get_year_high())
        self.assertIsNotNone(tdr)



if __name__ == '__main__':
    unittest.main()
