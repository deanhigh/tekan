from conf import MONGO
from mdl import DATE
from pymongo import MongoClient


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


def dataframe_to_mongo(df, symbol):
    with MongoClient(*MONGO) as mc:
        db = mc.get_database('quotes')
        col = get_collection(db, symbol)
        insert(col, df)

