'http://query.yahooapis.com/v1/public/yql'
from pprint import pprint

from pymongo import MongoClient
from pymongo.errors import BulkWriteError

from mdl import CSV_ROW, DATE
from mdl.ticker import Ticker

tickers = ['ADBE']
ts_range = ('2005-01-01', '2016-06-17')


def to_csv():
    import csv
    for t in tickers:
        ticker = Ticker(t)
        with open('{}.csv'.format(t), 'w') as f:
            csvw = csv.writer(f)
            csvw.writerow(CSV_ROW)
            for r in ticker.get_ts(CSV_ROW, ts_range):
                csvw.writerow([r[x] for x in CSV_ROW])


def bulk_insert(collection, data):
    try:
        collection.insert_many(data)
    except BulkWriteError as e:
        pprint(e.details)


def get_collection(db, name):
    col = db.get_collection(name)
    col.ensure_index(DATE, unique=True)
    return col


def to_mongo():
    mc = MongoClient('localhost', 27017)
    db = mc.get_database('quotes')
    for t in tickers:
        ticker = Ticker(t)
        col = get_collection(db, t)
        bulk_insert(col, ticker.get_ts(CSV_ROW, ts_range))


if __name__ == '__main__':
    to_mongo()
