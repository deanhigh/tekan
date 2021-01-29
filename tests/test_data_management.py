import os
import unittest

from ta.data_management.file_ds import FileSource
from ta.mdl import DataSet


class LoadAndSaveDataSets(unittest.TestCase):

    def test_load_dataset(self):
        ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))
        self.assertEqual(len(ds), 11352)


if __name__ == '__main__':
    unittest.main()
