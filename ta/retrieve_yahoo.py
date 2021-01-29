import argparse
import logging

import yaml

from ta.connectors.yahoo import YahooDataSource
from ta.data_management.file_ds import FileSource
from ta.mdl import DataSet


def get_symbols(symbol_file):
    with open(symbol_file) as f:
        yml = yaml.load(f)
        return [DataSet(s) for s in yml['symbols']]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    argsp = argparse.ArgumentParser('Retrieve data from sources and insert into mongo')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to retrieve')
    argsp.add_argument('-f', action='store', dest='symbols_file', default=False, help='Retrieve in symbols file')
    argsp.add_argument('-o', action='store', dest='output_file', default='output.csv', help='Output file')
    args = argsp.parse_args()

    ds = FileSource(args.output_file)
    if args.symbols_file:
        for s in get_symbols(args.symbols_file):
            YahooDataSource.load(args.symbol).save(ds)
    elif args.symbol:
        YahooDataSource.load(args.symbol).save(ds)
    else:
        argsp.print_help()
