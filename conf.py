import datetime

import yaml

NASDAQ_TICKER_URL = 'ftp://ftp.nasdaqtrader.com/symboldirectory/nasdaqtraded.txt'
MONGO = ('192.168.99.100', 27017)
TS_RANGE = (datetime.datetime(1900, 1, 1), datetime.date.today())
# TS_RANGE = (datetime.datetime(2010, 8, 24), datetime.datetime(2010, 10, 24))

def get_symbols(symbol_file='symbols.yml'):
    with open(symbol_file) as f:
        yml = yaml.load(f)
        return yml['symbols']

