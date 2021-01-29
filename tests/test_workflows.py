import os
import unittest

from pandas import DataFrame

from ta.data_management.file_ds import FileSource
from ta.db import ADJ_CLOSE, VOLUME, CLOSE, HIGH, LOW, OPEN
from ta.mdl.workflows import WorkflowContext, DuplicateTimeSeries, WorkflowLoader
from ta.indicators.kpi import *


# class TestWorkflowContextOperations(unittest.TestCase):
#     def setUp(self):
#         self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))
#
#     def test_add_series(self):
#         wc = WorkflowContext()
#         wc.add_ts_data(self.ds.data_frame[ADJ_CLOSE])
#         self.assertSetEqual(wc.ts_ids, {ADJ_CLOSE})
#
#     def test_add_data_frame(self):
#         wc = WorkflowContext()
#         wc.add_ts_data(self.ds.data_frame)
#         self.assertSetEqual(wc.ts_ids, {VOLUME, OPEN, LOW, HIGH, CLOSE, ADJ_CLOSE})
#
#     def test_fail_on_dupe(self):
#         wc = WorkflowContext()
#         wc.add_ts_data(self.ds.data_frame[ADJ_CLOSE])
#         try:
#             wc.add_ts_data(self.ds.data_frame[ADJ_CLOSE])
#         except DuplicateTimeSeries as e:
#             self.assertSetEqual(wc.ts_ids, {ADJ_CLOSE})
#             self.assertSetEqual({ADJ_CLOSE}, e.duplicate_columns)
#
#     def test_fail_on_dupe_dataframe(self):
#         wc = WorkflowContext()
#         wc.add_ts_data(self.ds.data_frame)
#         try:
#             new_df = DataFrame()
#             new_df += self.ds.data_frame[ADJ_CLOSE]
#             new_df += self.ds.data_frame[OPEN]
#         except DuplicateTimeSeries as e:
#             self.assertSetEqual(wc.ts_ids, {VOLUME, OPEN, LOW, HIGH, CLOSE, ADJ_CLOSE})
#             self.assertSetEqual({ADJ_CLOSE, OPEN}, e.duplicate_columns)


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
        self.assertSetEqual(set(self.wfl.get_datasets().keys()), {'SYM.OPEN', 'SYM.ADJ_CLOSE', 'SYM.MA20'})


class TestWorkflowContext(unittest.TestCase):

    def test_load_context(self):
        wc = WorkflowContext.load(WorkflowLoader.from_yaml(os.path.join(os.path.dirname(__file__), "./simple_workflow.yml")))
        self.assertSetEqual(set(wc.datasets.keys()), {'SYM.OPEN', 'SYM.ADJ_CLOSE', 'SYM.MA20'})

if __name__ == '__main__':
    unittest.main()
