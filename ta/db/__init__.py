import datetime

from mongoengine import *

HIGH = 'High'
LOW = 'Low'
OPEN = 'Open'
CLOSE = 'Close'
ADJ_CLOSE = 'Adj Close'
VOLUME = 'Volume'
SYMBOL = 'Symbol'
DATE = 'Date'

CSV_ROW = [SYMBOL, DATE, HIGH, LOW, OPEN, CLOSE, ADJ_CLOSE, VOLUME]

WFT_INPUT = 'input'
WFT_TRIGGER = 'trigger'
WFT_FUNCTION = 'function'


class Symbol(Document):
    ticker = StringField(required=True, unique=True)
    source = StringField(required=True)
    create_date = DateTimeField(default=datetime.datetime.utcnow())

    meta = {
        'db_alias': 'admin',
        'collection': 'symbols'
    }

    @classmethod
    def create(cls, ticker, source='yahoo'):
        return cls(ticker=ticker, source=source)


class TimeSeries(Document):
    cob = DateTimeField(required=True, unique=True)
    high = StringField(required=True)
    create_date = DateTimeField(default=datetime.datetime.utcnow())

    meta = {
        'db_alias': 'quotes',
        'indexes': ['cob']
    }

    @classmethod
    def create(cls, cob, high):
        return cls(cob=cob, high=high)


class Workflow(Document):
    name = StringField(required=True, unique=True)
    desc = StringField()
    create_date = DateTimeField(default=datetime.datetime.utcnow())

    meta = {
        'db_alias': 'admin',
        'collection': 'workflows'
    }

    @classmethod
    def create(cls, name):
        return cls(name=name)

