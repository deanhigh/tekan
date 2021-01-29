import argparse
import logging

import yaml

from ta.db.mongo_tools import add_symbol
from ta.mdl import Symbol


def get_symbols(symbol_file):
    with open(symbol_file) as f:
        yml = yaml.load(f)
        return [Symbol(s) for s in yml['symbols']]

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    argsp = argparse.ArgumentParser('Retrieve data from sources and insert into mongo')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to retrieve')
    argsp.add_argument('-f', action='store', dest='symbols_file', default=False, help='Retrieve in symbols file')
    args = argsp.parse_args()

    if args.symbols_file:
        for s in get_symbols(args.symbols_file):
            Symbol(ticker=s).save()
    elif args.symbol:
        Symbol(ticker=args.symbol).save()
    else:
        argsp.print_help()
