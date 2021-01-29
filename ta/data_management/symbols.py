from ta.connectors.yahoo import YahooDataSource
from ta.utils.yaml import YamlLoader


class SymbolsList(YamlLoader):

    """ Symbols list container """
    def __init__(self, symbols):
        self.symbols = symbols

    @classmethod
    def from_dict(cls, yml, range_start=None, range_end=None):
        return cls([YahooDataSource(s, range_start, range_end) for s in yml['symbols']])

    def __len__(self):
        return len(self.symbols)
