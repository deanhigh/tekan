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
        self.assertEqual(len(result.data_frame['EMA20']), 1892)
        self.assertEqual(len(result.data_frame['MA20']), 1892)