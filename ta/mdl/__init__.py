HIGH = 'High'
LOW = 'Low'
OPEN = 'Open'
CLOSE = 'Close'
ADJ_CLOSE = 'Adj Close'
VOLUME = 'Volume'
SYMBOL = 'Symbol'
DATE = 'Date'

CSV_ROW = [SYMBOL, DATE, HIGH, LOW, OPEN, CLOSE, ADJ_CLOSE, VOLUME]


class Symbol(object):
    def __init__(self, ticker):
        self.ticker = ticker
