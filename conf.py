import datetime

import yaml

NASDAQ_TICKER_URL = 'ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt'
MONGO = ('192.168.99.100', 27017)
TS_RANGE = (datetime.datetime(1900, 1, 1), datetime.date.today())


def get_symbols(symbol_file='symbols.yml'):
    with open(symbol_file) as f:
        yml = yaml.load(f)
        return yml['symbols']

