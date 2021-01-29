import unittest
from time import strptime

import numpy as np
import os

from pandas import DataFrame

from ta.data_management.file_ds import FileSource
from ta.db import ADJ_CLOSE
from ta.indicators import IndicatorDataSetWrapper
from ta.indicators.kpi import SMA, EMA
from ta.mdl import DataSet


class TestIndicatorsHappyPath(unittest.TestCase):

    def setUp(self):
        self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))

    def assert_indicator_structure(self, indicator, result):
        self.assertIsInstance(result, DataSet)
        self.assertEqual(result, indicator.data_set)

    def test_auto_calc_indicator(self):
        sma = SMA(self.ds, period=20, field=ADJ_CLOSE)
        self.assertEqual(sma.get_value('2016-12-28', 'MA20'), 95)

    def test_sma(self):
        sma = SMA(self.ds, period=20, field=ADJ_CLOSE)
        result = sma.calc()
        self.assert_indicator_structure(sma, result)
        self.assertEqual(len(result.data_frame['MA20']), 104)
        # I expect the first 19 to be NaN because of the window
        self.assertListEqual([np.isnan(x) for x in result.data_frame['MA20'][0:19]], [True] * 19)
        #  And the next 1872 should be False
        self.assertListEqual([np.isnan(x) for x in result.data_frame['MA20'][20:]], [False] * 84)
        self.assertEqual(sma.get_value('2016-12-28', 'MA20'), 95)


    def test_ema(self):
        ema = EMA(self.ds, period=20, field=ADJ_CLOSE)
        result = ema.calc()
        self.assert_indicator_structure(ema, result)
        self.assertEqual(len(result.data_frame['EMA20']), 104)
        # I expect the first 19 to be NaN because of the window
        self.assertListEqual([np.isnan(x) for x in result.data_frame['EMA20'][0:19]], [True] * 19)
        #  And the next 1872 should be False
        self.assertListEqual([np.isnan(x) for x in result.data_frame['EMA20'][20:]], [False] * 84)
        self.assertEqual(ema.get_value('2016-12-28', 'EMA20'), 95)

class TestJoinedIndicators(unittest.TestCase):
    def setUp(self):
        self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))

    def test_sma_ema(self):
        sma = SMA(self.ds, period=20, field=ADJ_CLOSE)
        ema = EMA(IndicatorDataSetWrapper('SMA', sma), period=20, field=ADJ_CLOSE)
        result = ema.calc()
        self.assertEqual(len(result.data_frame['EMA20']), 104)
        self.assertEqual(len(result.data_frame['MA20']), 104)

if __name__ == '__main__':
    unittest.main()
