import os
import unittest

from pandas import DataFrame

from ta.data_management.file_ds import FileSource
from ta.db import ADJ_CLOSE, VOLUME, CLOSE, HIGH, LOW, OPEN
from ta.mdl.workflows import WorkflowContext, DuplicateTimeSeries


class TestWorkflowContextOperations(unittest.TestCase):
    def setUp(self):
        self.ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))

    def test_add_series(self):
        wc = WorkflowContext()
        wc.add_ts_data(self.ds.data_frame[ADJ_CLOSE])
        self.assertSetEqual(wc.ts_ids, {ADJ_CLOSE})

    def test_add_data_frame(self):
        wc = WorkflowContext()
        wc.add_ts_data(self.ds.data_frame)
        self.assertSetEqual(wc.ts_ids, {VOLUME, OPEN, LOW, HIGH, CLOSE, ADJ_CLOSE})

    def test_fail_on_dupe(self):
        wc = WorkflowContext()
        wc.add_ts_data(self.ds.data_frame[ADJ_CLOSE])
        try:
            wc.add_ts_data(self.ds.data_frame[ADJ_CLOSE])
        except DuplicateTimeSeries as e:
            self.assertSetEqual(wc.ts_ids, {ADJ_CLOSE})
            self.assertSetEqual({ADJ_CLOSE}, e.duplicate_columns)

    def test_fail_on_dupe_dataframe(self):
        wc = WorkflowContext()
        wc.add_ts_data(self.ds.data_frame)
        try:
            new_df = DataFrame()
            new_df += self.ds.data_frame[ADJ_CLOSE]
            new_df += self.ds.data_frame[OPEN]
        except DuplicateTimeSeries as e:
            self.assertSetEqual(wc.ts_ids, {VOLUME, OPEN, LOW, HIGH, CLOSE, ADJ_CLOSE})
            self.assertSetEqual({ADJ_CLOSE, OPEN}, e.duplicate_columns)