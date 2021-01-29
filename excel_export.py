import argparse
import logging
import os

import pandas as pd
from conf import get_symbols
from kpi import MongoTickerSource

from logging import warning, info


def export_dataframe(df, output_filename, sheetname):
    info("Exporting %s", output_filename)
    writer = pd.ExcelWriter(output_filename, engine='xlsxwriter', date_format='yyyy/mm/dd',
                            datetime_format='yyyy/mm/dd')
    df.to_excel(writer, sheet_name=sheetname)
    writer.save()


def export_underlying(symbol, output_directory, output_filename=None):
    if not output_filename:
        output_filename = "{}.xlsx".format(symbol)

    with MongoTickerSource(symbol) as ts:
        if ts.exists():
            df = ts.underlying_df()
            export_dataframe(df, os.path.join(output_directory, output_filename), 'Underlying')
        else:
            warning("%s does not exist in mongodb", symbol)


def export_symbols_in_file(symbols_file, output_dir):
    for s in get_symbols(symbols_file):
        export_underlying(s, output_dir)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    argsp = argparse.ArgumentParser('Symbol exporter')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to dump to file')
    argsp.add_argument('-f', action='store', dest='symbols_file', default=False, help='Retrieve in symbols file')
    argsp.add_argument('-d', action='store', dest='out_dir', default='/Users/dean.high/Google Drive/Data/',
                       help='Directory to write data to')

    args = argsp.parse_args()
    if args.symbols_file:
        export_symbols_in_file(args.symbols_file, args.out_dir)
    elif args.symbol:
        export_underlying(args.symbol, args.out_dir)
    else:
        argsp.print_help()
