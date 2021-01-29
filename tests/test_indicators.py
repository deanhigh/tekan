import unittest

import numpy as np
import os
from ta.data_management.file_ds import FileSource
from ta.indicators.kpi import SMA

print()

class TestIndividualIndicatorsWrapped(unittest.TestCase):
    def setUp(self):
        self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))

    def test_sma(self):
        result = SMA.create_from_dataset(self.ds).calc()
        self.assertEqual(len(result.data_frame['MA20']), 1892)
        # I expect the first 19 to be NaN because of the window
        self.assertListEqual([np.isnan(x) for x in result.data_frame['MA20'][0:19]], [True] * 19)
        #  And the next 1872 should be False
        self.assertListEqual([np.isnan(x) for x in result.data_frame['MA20'][20:]], [False] * 1872)

    def test_ema(self):
        self.fail()


if __name__ == '__main__':
    unittest.main()
