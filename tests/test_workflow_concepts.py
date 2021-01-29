import os
import unittest

import numpy as np

from conf import get_full_data_path
from ta.data_management.file_ds import FileSource
from ta.indicators import *
from ta.mdl import Trigger, CallbackAction
from ta.mdl.workflows import WorkflowContext, WorkflowLoader
from ta.predicates import *
from ta.functions import *


class TestWorkflowLoading(unittest.TestCase):
    """ Tests the loading from yaml mechanism """
    def setUp(self):
        self.wfl = WorkflowLoader.from_yaml(os.path.join(os.path.dirname(__file__), "./simple_workflow.yml"))

    def test_load_filesource(self):
        wfl = self.wfl
        self.assertIsInstance(wfl.sources['SYM.LOADER'], FileSource)
        self.assertEqual(wfl.sources['SYM.LOADER'].id, 'SYM.LOADER')
        self.assertEqual(wfl.sources['SYM.LOADER'].filename, 'tests/test_data_frame.csv')

    def test_load_indicator(self):
        wfl = self.wfl
        self.assertIsInstance(wfl.indicators['SYM.MA20'], SMA)
        self.assertEqual(wfl.indicators['SYM.MA20'].id, 'SYM.MA20')
        self.assertEqual(wfl.indicators['SYM.MA20'].period, 20)
        self.assertEqual(wfl.indicators['SYM.MA20'].input_data_id, 'SYM.ADJ_CLOSE')

    def test_load_trigger(self):
        wfl = self.wfl
        trigger = wfl.triggers['SYM.MA20.GT_100']
        self.assertIsInstance( trigger, Trigger)
        self.assertEqual(trigger.id, 'SYM.MA20.GT_100')
        self.assertIsInstance(trigger.predicate, Expression )
        self.assertEqual(trigger.predicate.expression, 'input > value')
        self.assertEqual(trigger.predicate.value, 100)
        self.assertEqual(trigger.predicate.input, 'SYM.MA20.2016-12-28')

    def test_get_data_sets(self):
        self.assertSetEqual(set(self.wfl.get_data_pointers().keys()),
                            {'SYM.OPEN', 'SYM.ADJ_CLOSE', 'SYM.MA20', 'SYM.EMA20', 'SYM.EMA20_OF_MA20'})


class TestWorkflowContext(unittest.TestCase):
    def test_load_context(self):
        wc = WorkflowContext.load(
            WorkflowLoader.from_yaml(os.path.join(os.path.dirname(__file__), "./simple_workflow.yml")))
        self.assertSetEqual(set(wc.datasets.keys()),
                            {'SYM.OPEN', 'SYM.ADJ_CLOSE', 'SYM.MA20', 'SYM.EMA20_OF_MA20', 'SYM.EMA20', 'SYM.MA20.2016-12-28'})


class TestWorkflowContextIndicatorDependencies(unittest.TestCase):
    """ Tests that dependent data sources are loaded or calculated """
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml(get_full_data_path('tests/simple_workflow.yml')))

    def test_dependencies(self):
        self.assertEqual(104, len(self.wc.get_data('SYM.ADJ_CLOSE')))
        self.assertEqual(104, len(self.wc.get_data('SYM.OPEN')))
        self.assertEqual(104, len(self.wc.get_data('SYM.MA20')))


class TestJoinedData(unittest.TestCase):
    """ Tests calculating indicators off of other indicators """
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml(get_full_data_path('tests/simple_workflow.yml')))

    def test_ema_of_sma(self):
        self.assertEqual(104, len(self.wc.get_data('SYM.EMA20_OF_MA20')))
        self.assertEqual(1865.9251405475791, self.wc.get_data('SYM.EMA20_OF_MA20')['2016-12-28'])
        self.assertEqual(1823.3725237631138, self.wc.get_data('SYM.EMA20_OF_MA20')['2016-12-27'])
        self.assertListEqual([np.isnan(x) for x in self.wc.get_data('SYM.EMA20_OF_MA20')[0:38]], [True] * 38)
        self.assertListEqual([np.isnan(x) for x in self.wc.get_data('SYM.EMA20_OF_MA20')[39:]], [False] * 65)


class TestProcessingTrigger(unittest.TestCase):
    """ Tests calculating indicators off of other indicators """
    def setUp(self):
        self.wc = WorkflowContext.load(WorkflowLoader.from_yaml(get_full_data_path('tests/simple_workflow.yml')))

    def test_trigger(self):
        def callback(context):
            raise CallbackCalled()
        trigger = self.wc.get_trigger('SYM.MA20.GT_100')
        trigger.action = CallbackAction(callback)
        self.assertRaises(CallbackCalled, trigger.apply, self.wc)

    def test_trigger_log_alert(self):
        self.fail("Log an alert in the alert log when the trigger it true")


class CallbackCalled(Exception):
    def __init__(self):
        super(CallbackCalled, self).__init__()


class TestAction(unittest.TestCase):
    def test_callback_action(self):
        def callback(context):
            raise CallbackCalled()
        self.assertRaises( CallbackCalled, CallbackAction(callback).apply, None )


if __name__ == '__main__':
    unittest.main()
