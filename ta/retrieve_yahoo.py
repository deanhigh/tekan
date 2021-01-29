import argparse
import logging
import os

import yaml

from conf import TS_RANGE
from ta.connectors.yahoo import YahooDataSource
from ta.data_management.file_ds import CsvFileWriter
from ta.data_management.mongo_ds import DataFrameMongoWriter
from ta.data_management.symbols import SymbolsList
from ta.db.mongo_tools import get_source_ts_collection

log = logging.getLogger(__name__)

def save_mongo(sym):
    collection = get_source_ts_collection(sym.id)
    sym.load()
    sym.save(DataFrameMongoWriter(collection))


def save_file(sym):
    sym.load()
    sym.save(CsvFileWriter(os.path.join(args.output_dir, '%s.csv' % sym.id)))


if __name__ == '__main__':
    persistent_store_map = {
        'mongo': save_mongo,
        'file': save_file
    }

    logging.basicConfig(level=logging.INFO)

    argsp = argparse.ArgumentParser('Retrieve data from sources and write to file')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to retrieve')
    argsp.add_argument('-f', action='store', dest='symbols_file', default=False, help='Retrieve in symbols file')
    argsp.add_argument('-p', action='store', dest='persistent_store', default='file', help='Which persistent store to save the symbols to [file/mongo]')
    argsp.add_argument('-d', action='store', dest='output_dir', default='', help='Output dir')
    args = argsp.parse_args()

    if args.symbols_file:
        for yds in SymbolsList.from_yaml(args.symbols_file):
            try:
                persistent_store_map[args.persistent_store](yds)
            except IOError as e:
                log.error("Unable to retrieve data for symbol %s" % yds.id, e)
    elif args.symbol:
        yds = YahooDataSource(args.symbol, *TS_RANGE)
        persistent_store_map[args.persistent_store](yds)

    else:
        argsp.print_help()
