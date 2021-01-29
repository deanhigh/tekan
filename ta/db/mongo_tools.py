from functools import partial
from logging import warning

from pymongo import MongoClient

from conf import MONGO
from sources import MongoTickerSource
from ta.db import Symbol, DATE, Workflow
import logging

log = logging.getLogger("mongo-tools")

ADMIN_DB = 'admin'
SYMBOLS_COL = 'symbols'
WORKFLOW_COL = 'workflows'
WORKFLOW_NODES_COL = 'workflow_nodes'

TS_DB = 'source_ts'


mc = MongoClient(*MONGO)


def get_ts_collection(database, collection_name):
    db = mc.get_database(TS_DB)
    col = db.get_collection(collection_name)
    col.ensure_index(DATE, unique=True)
    return col

get_source_ts_collection = partial(get_ts_collection, TS_DB)


def dataframe_to_mongo(df, symbol, overwrite=False):
    """Insert a data frame into a collection"""
    db = mc.get_database(TS_DB)
    col = db.get_collection(symbol)
    col.ensure_index(DATE, unique=True)
    for ts, data in df.to_dict('index').items():
        data[DATE] = ts.to_datetime()
        if data[DATE]:
            col.insert(data)
        else:
            log.error('error, no date {}', data)

def get_time_series(ticker):
    ts = MongoTickerSource(mc, ticker)
    if ts.exists():
        return ts.underlying_df()
    else:
        warning("%s does not exist in repository", ticker)


def get_symbols():
    return [x for x in Symbol.objects()]


def get_symbol(ticker):
    return Symbol.objects(ticker=ticker).first()


def create_symbol(symbol):
    if type(symbol) is Symbol:
        symbol.save()
    else:
        raise TypeError('Unable to store type %s as symbol' % type(symbol))


def delete_symbol(ticker):
    s = Symbol.objects(ticker=ticker)
    s.delete()


def create_workflow(workflow):
    if type(workflow) is Workflow:
        workflow.save()
    else:
        raise TypeError('Unable to store type %s as workflow' % type(workflow))


def delete_workflow(workflow_name):
    s = Workflow.objects(name=workflow_name)
    s.delete()


def get_workflows():
    return [x for x in Workflow.objects()]


def get_workflow(name):
    return Workflow.objects(name=name).first()
