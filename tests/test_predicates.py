import unittest
from unittest.mock import MagicMock

from ta.mdl.workflows import WorkflowContext
from ta.predicates import Expression


class TestSimplePredicates(unittest.TestCase):
    def test_greater_than_trigger(self):
        wc = WorkflowContext()
        wc.get_data = MagicMock(return_value=3)
        self.assertTrue(Expression('value > input', {'function', 'TEST'}, 10).apply(wc))
