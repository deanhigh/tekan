import argparse
import logging
from logging import info, exception

from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError

from conf import TS_RANGE, get_symbols
from ta.db import dataframe_to_mongo


def fetch_symbol_data(symbol):
    info("Fetching underlying data for %s", symbol)
    df = data.DataReader(symbol, 'yahoo', *TS_RANGE)
    dataframe_to_mongo(df, symbol, True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    argsp = argparse.ArgumentParser('Retrieve data from sources and insert into mongo')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to retrieve')
    argsp.add_argument('-f', action='store', dest='symbols_file', default=False, help='Retrieve in symbols file')
    args = argsp.parse_args()

    if args.symbols_file:
        for s in get_symbols(args.symbols_file):
            try:
                fetch_symbol_data(s)
            except RemoteDataError as e:
                exception("Error fetching symbol %s", s)
    elif args.symbol:
        fetch_symbol_data(args.symbol)
    else:
        argsp.print_help()
