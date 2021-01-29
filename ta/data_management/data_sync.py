from logging import info

from pandas_datareader import data

from conf import TS_RANGE
from ta.db.mongo_tools import dataframe_to_mongo, get_symbols


def fetch_symbol_data(symbol):
    info("Fetching underlying data for %s", symbol)
    df = data.DataReader(symbol, 'yahoo', *TS_RANGE)
    dataframe_to_mongo(df, symbol, True)


def fetch_all_symbols():
    for symbol in get_symbols():
        fetch_symbol_data(symbol)


