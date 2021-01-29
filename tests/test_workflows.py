import os
import unittest

import numpy as np

from ta.data_management.file_ds import FileSource
from ta.indicators.kpi import *
from ta.mdl.workflows import WorkflowContext, WorkflowLoader

class TestWorkflowLoader(unittest.TestCase):
    def setUp(self):
        self.wfl = WorkflowLoader.from_yaml(os.path.join(os.path.dirname(__file__), "./simple_workflow.yml"))

    def test_load_yaml(self):
        wfl = self.wfl
        self.assertEqual(type(wfl.sources['SYM.LOADER']), FileSource)
        self.assertEqual(wfl.sources['SYM.LOADER'].id, 'SYM.LOADER')
        self.assertEqual(wfl.sources['SYM.LOADER'].filename, 'test_data_frame.csv')

        self.assertEqual(type(wfl.indicators['SYM.MA20']), SMA)
        self.assertEqual(wfl.indicators['SYM.MA20'].id, 'SYM.MA20')
        self.assertEqual(wfl.indicators['SYM.MA20'].period, 20)
        self.assertEqual(wfl.indicators['SYM.MA20'].input_data_id, 'SYM.ADJ_CLOSE')

    def test_get_data_sets(self):
        self.assertSetEqual(set(self.wfl.get_data_pointers().keys()),
                            {'SYM.OPEN', 'SYM.ADJ_CLOSE', 'SYM.MA20', 'SYM.EMA20', 'SYM.EMA20_OF_MA20'})


class TestWorkflowContext(unittest.TestCase):
    def test_load_context(self):
        wc = WorkflowContext.load(
            WorkflowLoader.from_yaml(os.path.join(os.path.dirname(__file__), "./simple_workflow.yml")))
        self.assertSetEqual(set(wc.datasets.keys()),
                            {'SYM.OPEN', 'SYM.ADJ_CLOSE', 'SYM.MA20', 'SYM.EMA20_OF_MA20', 'SYM.EMA20'})


class TestWorkflowContextIndicatorDependencies(unittest.TestCase):
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml('simple_workflow.yml'))

    def test_dependencies(self):
        self.assertEqual(104, len(self.wc.get_data('SYM.ADJ_CLOSE')))
        self.assertEqual(104, len(self.wc.get_data('SYM.OPEN')))
        self.assertEqual(104, len(self.wc.get_data('SYM.MA20')))


class TestJoinedData(unittest.TestCase):
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml('simple_workflow.yml'))

    def test_ema_of_sma(self):
        self.assertEqual(104, len(self.wc.get_data('SYM.EMA20_OF_MA20')))
        self.assertEqual(1865.9251405475791, self.wc.get_data('SYM.EMA20_OF_MA20')['2016-12-28'])
        self.assertEqual(1823.3725237631138, self.wc.get_data('SYM.EMA20_OF_MA20')['2016-12-27'])
        self.assertListEqual([np.isnan(x) for x in self.wc.get_data('SYM.EMA20_OF_MA20')[0:38]], [True] * 38)
        self.assertListEqual([np.isnan(x) for x in self.wc.get_data('SYM.EMA20_OF_MA20')[39:]], [False] * 65)


class TestIndicatorsFromContextLoad(unittest.TestCase):
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml('simple_workflow.yml'))

    def test_sma(self):
        self.assertEqual(104, len(self.wc.get_data('SYM.MA20')))
        self.assertEqual(2270.1749999999997, self.wc.get_data('SYM.MA20')['2016-12-28'])
        self.assertEqual(2222.8749999999995, self.wc.get_data('SYM.MA20')['2016-12-27'])

    def test_ema(self):
        self.assertEqual(104, len(self.wc.get_data('SYM.EMA20')))
        self.assertEqual(2286.7962876973415, self.wc.get_data('SYM.EMA20')['2016-12-28'])
        self.assertEqual(2239.4958969286408, self.wc.get_data('SYM.EMA20')['2016-12-27'])


if __name__ == '__main__':
    unittest.main()
