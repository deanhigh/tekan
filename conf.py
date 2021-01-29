import datetime
import os
from configparser import ConfigParser

import yaml


NASDAQ_TICKER_URL = 'ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt'
MONGO =  ('127.0.0.1', 27017)#('192.168.99.100', 27017)
TS_RANGE = (datetime.datetime(1900, 1, 1), datetime.date.today())

DATA_DIR=os.path.dirname(__file__)


def get_full_data_path(path):
    return os.path.join(DATA_DIR, path)
