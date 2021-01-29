from pymongo import MongoClient

from conf import MONGO
from ta.mdl import DATE


def insert(collection, df):
    for ts, data in df.to_dict('index').items():
        data[DATE] = ts.to_datetime()
        if data[DATE]:
            collection.insert(data)
        else:
            print('error, no date {}', data)


def get_collection(db, name, drop_col=False):
    col = db.get_collection(name)
    if drop_col:
        col.drop()
    col.ensure_index(DATE, unique=True)
    return col


def dataframe_to_mongo(df, symbol, overwrite=False):
    with MongoClient(*MONGO) as mc:
        db = mc.get_database('quotes')
        col = get_collection(db, symbol, overwrite)
        insert(col, df)


def get_symbols():
    with MongoClient(*MONGO) as mc:
        db = mc.get_database('admin')
        col = db.get_collection('symbols')
        col.ensure_index('ticker')
        return [x for x in col.find()]


def add_symbol(ticker):
    with MongoClient(*MONGO) as mc:
        db = mc.get_database('admin')
        col = db.get_collection('symbols')
        col.ensure_index('ticker')
        col.insert(ticker)
        return col


def delete_symbol(ticker):
    with MongoClient(*MONGO) as mc:
        db = mc.get_database('admin')
        col = db.get_collection('symbols')
        col.ensure_index('ticker')
        return col.delete_many({'ticker': ticker})
