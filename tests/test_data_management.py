import os
import unittest

from ta.data_management.file_ds import FileSource
from ta.data_management.symbols import SymbolsList


class LoadAndSaveDataSets(unittest.TestCase):
    def test_load_dataset(self):
        ds = FileSource("TEST", os.path.join(os.path.dirname(__file__), "./test_data_frame.csv"))
        self.assertEqual(len(ds), 624)


class SymbolsListTest(unittest.TestCase):
    def test_load_dataset(self):
        symbols = SymbolsList.from_yaml(os.path.join(os.path.dirname(__file__), "./sample_symbols.yml"))
        self.assertEqual(5,len(symbols))
        self.assertListEqual(['^GSPC', 'SSO', 'UPRO', 'SPXS', 'SDS'], [str(i) for i in symbols.symbols])

if __name__ == '__main__':
    unittest.main()
