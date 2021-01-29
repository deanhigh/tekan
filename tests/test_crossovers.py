import unittest
from time import strptime

import pandas as pd

from ta.indicators.crossovers import CrossOver, CrossUnder
from ta.mdl import DataSet, Series


class TestJoinedIndicators(unittest.TestCase):

    def test_crossover_and_under(self):
        idx = [strptime(x, '%Y-%m-%d') for x in ['2017-01-05', '2017-01-06']]
        ds = DataSet('TEST')
        ds.data_frame = pd.DataFrame(
            {'A': pd.Series([3., 5.], index=idx),
             'B': pd.Series([3., 4.], index=idx)})
        self.assertTrue(CrossOver(Series(ds, 'A'), Series(ds, 'B')).apply(idx[1]))
        self.assertTrue(CrossUnder(Series(ds, 'B'), Series(ds, 'A')).apply(idx[1]))

    # def test_crossover(self):
    #     sma_20 = SMA(self.ds, period=20, field=ADJ_CLOSE)
    #     sma_40 = SMA(IndicatorDataSetWrapper('MA20', sma_20), period=40, field=ADJ_CLOSE)
    #     result = sma_40.calc()
    #
    #     previous_20 = result.data_frame['MA20'].shift(1)
    #     previous_40 = result.data_frame['MA40'].shift(1)
    #     crossing = (((result.data_frame['MA20'] <= result.data_frame['MA40']) & (previous_20 >= previous_40))
    #                 | ((result.data_frame['MA20'] >= result.data_frame['MA40']) & (previous_20 <= previous_40)))
    #
    #     self.assertEqual(list(crossing.values).count(True), 46)
