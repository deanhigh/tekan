'http://query.yahooapis.com/v1/public/yql'
import argparse

import pandas_datareader.data as web
import yaml
from conf import TS_RANGE
from mongo_tools import dataframe_to_mongo


def get_symbols(symbol_file='symbols.yml'):
    with open(symbol_file) as f:
        yml = yaml.load(f)
        return yml['symbols']


def fetch_symbol_data(symbol):
    df = web.DataReader(symbol, 'yahoo', *TS_RANGE)
    dataframe_to_mongo(df, symbol)


if __name__ == '__main__':
    argsp = argparse.ArgumentParser('Retrieve data from sources and insert into mongo')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to retrieve')
    argsp.add_argument('-f', action='store_true', dest='symbols_file', default=False, help='Retrieve in symbols file')
    args = argsp.parse_args()

    if args.symbols_file:
        for s in get_symbols(args.symbols_file):
            fetch_symbol_data(s)
    elif args.symbol:
        fetch_symbol_data(args.symbol)
    else:
        argsp.print_help()

