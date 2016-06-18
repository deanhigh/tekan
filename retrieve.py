'http://query.yahooapis.com/v1/public/yql'
import csv

from mdl import CSV_ROW
from mdl.ticker import Ticker

tickers = ['ADBE']
ts_range = ('2016-01-01', '2016-01-31')

for t in tickers:
    ticker = Ticker(t)
    with open('{}.csv'.format(t), 'w') as f:
        csvw = csv.writer(f)
        csvw.writerow(CSV_ROW)
        for r in ticker.get_ts(CSV_ROW, ts_range):
            csvw.writerow([r[x] for x in CSV_ROW])
