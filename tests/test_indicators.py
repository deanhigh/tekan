import logging
import unittest

from ddt import ddt, unpack, data

from ta.indicators import *
from ta.mdl.workflows import WorkflowContext, WorkflowLoader

SYM_ADJ_CLOSE = 'SYM.ADJ_CLOSE'

log = logging.getLogger("test_indicators")

basic_test_data = [
    {'ind_name': 'SYM.MA20', 'ind_cls': SMA, 'test_points': {'2016-12-28': 2270.1749999999997}},
    {'ind_name': 'SYM.EMA20', 'ind_cls': EMA, 'test_points': {'2016-12-28': 2286.7962876973415}},
    {'ind_name': 'SYM.STDDEV20', 'ind_cls': STDDEV, 'test_points': {'2016-12-28': 274.28670333248476}},
    {'ind_name': 'SYM.TR', 'ind_cls': TR, 'test_points': {'2016-12-28': 2580.0899999999997}},
    {'ind_name': 'SYM.ATR', 'ind_cls': ATR, 'test_points': {'2016-12-28': 1799.2082310527996}},
    {'ind_name': 'SYM.NATR', 'ind_cls': NATR, 'test_points': {'2016-12-28': 65.756929665873571}},
]


@ddt
class TestIndicators(unittest.TestCase):
    def setUp(self):
        self.wfl = WorkflowLoader.from_yaml('all_indicators_test.yml')
        self.wc = WorkflowContext.load(self.wfl)

    @unpack
    @data(*basic_test_data)
    def test_indicators(self, ind_name, ind_cls, test_points, result_cls=Series, length=104):
        log.info("Testing %s", ind_name)
        result = self.wc.get_data(ind_name)
        self.assertIsInstance(self.wfl.indicators[ind_name], ind_cls)
        self.assertIsInstance(result, result_cls)
        self.assertEqual(len(result), length)
        for p in test_points.items():
            self.assertEqual(result[p[0]], p[1])


if __name__ == '__main__':
    unittest.main()
