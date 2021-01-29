from logging import info

from pandas_datareader import data

from conf import TS_RANGE
from ta.db.mongo_tools import dataframe_to_mongo, get_symbols


def fetch_symbol_data(symbol):
    info("Fetching underlying data for %s", symbol)
    df = data.DataReader(symbol.ticker, 'yahoo', *TS_RANGE)
    dataframe_to_mongo(df, symbol.ticker, True)


def fetch_all_symbols_data():
    for symbol in get_symbols():
        fetch_symbol_data(symbol)

if __name__ == '__main__':
    fetch_all_symbols_data()
