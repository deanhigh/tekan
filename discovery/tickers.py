# import csv
# import os
# from time import sleep
# from yahoo_finance import Share
#
# import py2neo
#
# class Ticker_(Share):
#     def __init__(self, symbol, name):
#         self.name = name
#         self.symbol = symbol
#
#     def __str__(self):
#         return self.symbol
#
#
# class TickerList(object):
#     def __init__(self, l=[]):
#         pass
#
#     @classmethod
#     def load_from_file(cls, filename):
#         res = []
#         with open(filename) as f:
#             rows = csv.reader(f, delimiter='|')
#             header = True
#             for row in rows:
#
#                 symbol = row[1]
#
#                 if header:
#                     header = False
#                     continue
#
#                 if len(row) < 8 or '$' in symbol:
#                     continue
#
#                 print "Loading %s " % symbol
#                 try:
#                     s = Ticker(symbol, row[2])
#                     res.append(s)
#                 except:
#                     print "Issue loading %s" % symbol
#
#         return res
#
#
# g = py2neo.Graph('http://neo4j:password@localhost:7474/db/data/')
# tx = g.cypher.begin()
# for t in TickerList.load_from_file('ticker_list.txt'):
#     tx.append("CREATE (ticker:Ticker {symbol:{symbol}, name:{name}})", name=t.name, symbol=t.symbol)
#     tx.append()
# tx.commit()