import argparse
import logging
import os

import yaml

from conf import TS_RANGE
from ta.connectors.yahoo import YahooDataSource
from ta.data_management.file_ds import CsvFileWriter
from ta.data_management.symbols import SymbolsList

log = logging.getLogger(__name__)





if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    argsp = argparse.ArgumentParser('Retrieve data from sources and write to file')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to retrieve')
    argsp.add_argument('-f', action='store', dest='symbols_file', default=False, help='Retrieve in symbols file')
    argsp.add_argument('-o', action='store', dest='output_file', default=None, help='Output file')
    argsp.add_argument('-d', action='store', dest='output_dir', default='', help='Output dir')
    args = argsp.parse_args()

    if args.symbols_file:
        for yds in SymbolsList.from_yaml(args.symbols_file):
            try:
                yds.load()
                yds.save(CsvFileWriter(os.path.join(args.output_dir, '%s.csv' % yds.id)))
            except IOError as e:
                log.error("Unable to retrieve data for symbol %s" % yds.id, e)
    elif args.symbol:
        yds = YahooDataSource(args.symbol, *TS_RANGE)
        yds.load()
        yds.save(CsvFileWriter(
            os.path.join(args.output_dir, args.output_file) if args.output_file else os.path.join(args.output_dir,
                                                                                                  '%s.csv' % yds.id)))
    else:
        argsp.print_help()
