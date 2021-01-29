import datetime

import yaml

NASDAQ_TICKER_URL = 'ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt'
MONGO = ('192.168.99.100', 27017)
TS_RANGE = (datetime.datetime(2009, 2, 11), datetime.datetime(2010, 5, 1))

def get_symbols(symbol_file='symbols.yml'):
    with open(symbol_file) as f:
        yml = yaml.load(f)
        return yml['symbols']

