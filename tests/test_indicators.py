import os
import unittest

import numpy as np
from pandas import Series

from ta.data_management.file_ds import FileSource
from ta.db import ADJ_CLOSE
from ta.indicators import IndicatorDataSetWrapper
from ta.indicators.kpi import SMA, EMA
from ta.mdl import DataSet
from ta.mdl.workflows import WorkflowContext, WorkflowLoader

SYM_ADJ_CLOSE = 'SYM.ADJ_CLOSE'


class TestIndicatorsHappyPath(unittest.TestCase):
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml('simple_workflow.yml'))

    def assert_indicator_structure(self, indicator, result):
        self.assertIsInstance(result, Series)

    def test_sma(self):
        sma = SMA('SMA20', SYM_ADJ_CLOSE, 20)
        result = sma.calc(self.wc)
        self.assert_indicator_structure(sma, result)
        self.assertEqual(len(result), 104)
        # I expect the first 19 to be NaN because of the window
        self.assertListEqual([np.isnan(x) for x in result[0:19]], [True] * 19)
        #  And the next 1872 should be False
        self.assertListEqual([np.isnan(x) for x in result[20:]], [False] * 84)
        self.assertEqual(result['2016-12-28'], 95)

    def test_ema(self):
        ema = EMA('EMA20', SYM_ADJ_CLOSE, 20)
        result = ema.calc(self.wc)
        self.assert_indicator_structure(ema, result)
        self.assertEqual(len(result), 104)
        # I expect the first 19 to be NaN because of the window
        self.assertListEqual([np.isnan(x) for x in result[0:19]], [True] * 19)
        #  And the next 1872 should be False
        self.assertListEqual([np.isnan(x) for x in result[20:]], [False] * 84)
        self.assertEqual(result['2016-12-28'], 95)


class TestJoinedIndicators(unittest.TestCase):
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml('simple_workflow.yml'))

    def test_sma_ema(self):
        sma = SMA('SMA20', SYM_ADJ_CLOSE, 20)
        ema = EMA('EMA20', 'SMA20', 20)
        result = ema.calc(self.wc)
        self.assertEqual(len(result.data_frame['EMA20']), 104)
        self.assertEqual(len(result.data_frame['MA20']), 104)


if __name__ == '__main__':
    unittest.main()
