import unittest

from mongoengine import connect, NotUniqueError
from mongoengine.connection import disconnect

# from ta.db import mongo_tools

# mongo_tools.mc = mongomock.MongoClient()
from ta.db import Symbol, Workflow
import ta.db.mongo_tools as mongo_tools


class SymbolTest(unittest.TestCase):
    def setUp(self):
        disconnect('admin')
        connect('admin', host='mongomock://localhost', alias='admin')
        self.assertEqual([], mongo_tools.get_symbols())

    def tearDown(self):
        disconnect('admin')
        self.assertEqual([], mongo_tools.get_symbols())

    def test_write_wrong_type(self):
        with self.assertRaises(TypeError):
            mongo_tools.create_symbol('TEST')

    def test_crud(self):
        """ Test crud operations"""
        # create
        s1 = Symbol.create('TEST1')
        s2 = Symbol.create('TEST2')
        mongo_tools.create_symbol(s1)
        mongo_tools.create_symbol(s2)
        # read
        self.assertEqual([s1, s2], mongo_tools.get_symbols())
        # update
        mongo_tools.get_symbol('TEST2').update(source='other')
        s2 = mongo_tools.get_symbol('TEST2')
        # delete
        mongo_tools.delete_symbol(s1.ticker)
        self.assertEqual([s2], mongo_tools.get_symbols())
        mongo_tools.delete_symbol(s2.ticker)

    def test_no_duplicates(self):
        """ We do not allow duplicates """
        # create
        s1 = Symbol.create('TEST1')
        s1.save()
        with self.assertRaises(NotUniqueError):
            Symbol.create('TEST1').save()

        # read
        self.assertEqual([s1], mongo_tools.get_symbols())
        # delete
        mongo_tools.delete_symbol(s1.ticker)


class WorkflowTest(unittest.TestCase):
    def setUp(self):
        disconnect('admin')
        connect('admin', host='mongomock://localhost', alias='admin')
        self.assertEqual([], mongo_tools.get_workflows())

    def tearDown(self):
        disconnect('admin')
        self.assertEqual([], mongo_tools.get_workflows())

    def test_write_wrong_type(self):
        with self.assertRaises(TypeError) as te:
            mongo_tools.create_workflow('TEST')

    def test_crud(self):
        """ Test crud operations"""
        # create
        w1 = Workflow.create('TEST1')
        w2 = Workflow.create('TEST2')
        mongo_tools.create_workflow(w1)
        mongo_tools.create_workflow(w2)
        # read
        self.assertEqual([w1, w2], mongo_tools.get_workflows())
        # update
        mongo_tools.get_workflow('TEST2').update(desc='description')
        w2 = mongo_tools.get_workflow('TEST2')
        # delete
        mongo_tools.delete_workflow(w1.name)
        self.assertEqual([w2], mongo_tools.get_workflows())
        mongo_tools.delete_workflow(w2.name)

    def test_no_duplicates(self):
        """ We do not allow duplicates """
        """ We do not allow duplicates """
        # create
        s1 = Workflow.create('TEST1').save()
        with self.assertRaises(NotUniqueError):
            Workflow.create('TEST1').save()

        # read
        self.assertEqual([s1], mongo_tools.get_workflows())
        # delete
        mongo_tools.delete_workflow(s1.name)


if __name__ == '__main__':
    unittest.main()
