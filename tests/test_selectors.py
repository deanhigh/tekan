import unittest
from unittest.mock import MagicMock

from pandas import Series

from ta.functions import TimeSeriesSelector
from ta.mdl.workflows import WorkflowContext


class TestSimpleSelectors(unittest.TestCase):

    def test_date_selector(self):
        wc = WorkflowContext()
        wc.get_data = MagicMock(return_value=Series([3], index=['2016-01-01']))
        self.assertEqual(3, TimeSeriesSelector('ID', 'TSERIES', '2016-01-01').apply(wc))