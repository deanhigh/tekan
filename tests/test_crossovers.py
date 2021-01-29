import unittest
from time import strptime

import pandas as pd

from ta.indicators.crossovers import CrossOver, CrossUnder
from ta.mdl import DataSet, SeriesPointer


class TestJoinedIndicators(unittest.TestCase):

    def test_crossover_and_under(self):
        idx = [strptime(x, '%Y-%m-%d') for x in ['2017-01-05', '2017-01-06']]
        ds = DataSet('TEST')
        ds.data_frame = pd.DataFrame(
            {'A': pd.Series([3., 5.], index=idx),
             'B': pd.Series([3., 4.], index=idx)})
        self.assertTrue(CrossOver(SeriesPointer(ds, 'A'), SeriesPointer(ds, 'B')).apply(idx[1]))
        self.assertTrue(CrossUnder(SeriesPointer(ds, 'B'), SeriesPointer(ds, 'A')).apply(idx[1]))
