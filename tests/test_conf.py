import unittest

import conf


class TestConfig(unittest.TestCase):
    def test_read_symbols(self):
        symbols = conf.get_symbols()['symbols']
        self.assertGreater(len(symbols), 2)


if __name__ == '__main__':
    unittest.main()
