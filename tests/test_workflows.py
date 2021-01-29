import os
import unittest

from ta.data_management.file_ds import FileSource
from ta.db import ADJ_CLOSE
from ta.indicators import IndicatorDataSetWrapper
from ta.indicators.kpi import SMA, EMA


class TestJoinedIndicators(unittest.TestCase):
    def setUp(self):
        self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))

    def test_sma_ema(self):
        sma = SMA(self.ds, period=20, field=ADJ_CLOSE)
        ema = EMA(IndicatorDataSetWrapper('SMA', sma), period=20, field=ADJ_CLOSE)
        result = ema.calc()
        self.assertEqual(len(result.data_frame['EMA20']), 104)
        self.assertEqual(len(result.data_frame['MA20']), 104)

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
