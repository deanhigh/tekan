import unittest

import matplotlib.pyplot as plt
from ddt import ddt, data
from indicators.kpi import SMA, EWMA, MarketVolatilityType
from mdl import ADJ_CLOSE
from tests import TestTickerSource

test_symbols = ['AAPL']


@ddt
class TestSMA(unittest.TestCase):
    @data(*test_symbols)
    def test_sma_png(self, symbol):
        with TestTickerSource(symbol) as t:
            t.underlying_field_df(ADJ_CLOSE).join(SMA.create(t).calc()).join(SMA.create(t).calc(50)).join(
                SMA.create(t).calc(100)).plot()
            plt.savefig('out_sma.png')

    @data(*test_symbols)
    def test_ewma_png(self, symbol):
        with TestTickerSource(symbol) as t:
            t.underlying_field_df(ADJ_CLOSE).join(EWMA.create(t).calc()).join(EWMA.create(t).calc(50)).join(
                EWMA.create(t).calc(100)).plot()
            plt.savefig('out_ewma.png')

    @data(*test_symbols)
    def test_ewma_png(self, symbol):
        with TestTickerSource(symbol) as t:
            mvt = MarketVolatilityType.create(t).calc(20)

            print(mvt.loc['20070710':'20070720'])
            # t.underlying_field_df(ADJ_CLOSE).join(EWMA.create(t).calc()).join(EWMA.create(t).calc(50)).join(
            #     .create(t).calc(100)).plot()
            # savefig('out_ewma.png')

if __name__ == '__main__':
    plt.style.use('dark_background')
    unittest.main()
