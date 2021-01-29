import unittest

import numpy as np
import talib
import os
from pandas import Series

from ta.data_management.file_ds import FileSource
from ta.db import ADJ_CLOSE, CLOSE
from ta.mdl import DataSet


class TestTALibFunctions(unittest.TestCase):
    def test_basic(self):
        # Relatively pointless test to check that TA Lib seems to function as expected with an ndarray
        sample = np.random.random(15)
        output = talib.SMA(sample, timeperiod=10)
        # I expect the first 9 to be NaN because of the window
        self.assertListEqual([np.isnan(x) for x in output[0:9]], [True]*9)
        #  And the next 5 should be False
        self.assertListEqual([np.isnan(x) for x in output[10:]], [False] * 5)
