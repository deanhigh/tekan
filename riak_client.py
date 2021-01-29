import datetime

from pandas import DataFrame
from riak.client import RiakClient

# NB: modify 'host' and 'pb_port' to match your installation
from ta.connectors.yahoo import YahooDataSource
from ta.db import OPEN, CLOSE, LOW, HIGH, ADJ_CLOSE, VOLUME

client = RiakClient(host='localhost', pb_port=8087)

""" CREATE TABLE DailyTickers
(
  symbol       VARCHAR   NOT NULL,
  time         TIMESTAMP NOT NULL,
  open         DOUBLE,
  close        DOUBLE,
  low          DOUBLE,
  high         DOUBLE,
  adj_close    DOUBLE,
  volume       DOUBLE,
  PRIMARY KEY (
    (symbol, QUANTUM(time, 1, 'd')), symbol, time DESC)
);
"""
#
# yds = YahooDataSource('AAPL', datetime.datetime.today() - datetime.timedelta(days=1000))
# yds.load()
#
# table = client.table('DailyTickers')
#
# rows = []
# for i in yds.data_frame.iterrows():
#     r = [yds.id, i[0], i[1].get(OPEN), i[1].get(CLOSE), i[1].get(LOW), i[1].get(HIGH), i[1].get(ADJ_CLOSE), i[1].get(VOLUME)]
#     rows.append(r)
#
# print(rows)
# ts_obj = table.new(rows)
# print("Store result:", ts_obj.store())

# fmt = "select open, close from DailyTickers where time > {t1} and time < {t2} and symbol = 'AAPL'"
# query = fmt.format(t1=(datetime.datetime.today() - datetime.timedelta(days=1000)).strftime('%s'), t2=datetime.datetime.today().strftime('%s'))
# print(query)
# ts_obj = client.ts_query('DailyTickers', query)
#
# print(dir(ts_obj))