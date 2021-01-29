import argparse
import pandas as pd

import sys

import xlsxwriter as xlsxwriter
from kpi import MongoTickerSource
from mdl import HIGH, ADJ_CLOSE, CLOSE, OPEN, LOW, DATE, VOLUME


def export_dataframe(df, output_filename, sheetname):
    writer = pd.ExcelWriter(output_filename, engine='xlsxwriter', date_format='yyyy/mm/dd', datetime_format='yyyy/mm/dd')
    df.to_excel(writer, sheet_name=sheetname)
    writer.save()


def export_underlying(symbol, output_filename=None):
    if not output_filename:
        output_filename = "{}.xlsx".format(symbol)

    with MongoTickerSource(symbol) as ts:
        df = ts.underlying_df()
        export_dataframe(df, output_filename, 'Underlying')


if __name__ == '__main__':
    argsp = argparse.ArgumentParser('Symbol exporter')
    argsp.add_argument('-s', action='store', dest='symbol', help='Symbol to dump to file')
    args = argsp.parse_args()
    export_underlying(args.symbol)
