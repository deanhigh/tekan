import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
import pymongo

from mdl import DATE, HIGH, CLOSE, ADJ_CLOSE, LOW, OPEN, VOLUME

def moving_average(ticker):
    with MongoClient('localhost', 27017) as mc:
        col = mc.get_database('quotes').get_collection(ticker)
        #print ([(i[DATE], i[HIGH]) for i in col.find()])
        df = pd.DataFrame(data=[i[HIGH] for i in col.find()], index=pd.DatetimeIndex([i[DATE]for i in col.find()]), dtype=float)
        #print(df.values)
        # ax = df.plot()
        # df.rolling(50).mean().plot(ax=ax)
        # plt.show()

def get_ticker_std(ticker):
    with MongoClient('localhost', 27017) as mc:
        col = mc.get_database('quotes').get_collection(ticker)
        #print ([(i[DATE], i[HIGH]) for i in col.find()])

        df = pd.DataFrame(data=[(i[HIGH], i[LOW], i[OPEN], i[CLOSE], i[ADJ_CLOSE]) for i in col.find()], index=pd.DatetimeIndex([i[DATE]for i in col.find()]), dtype=float)
        print(df.values)
        ax = df.plot()
        df.rolling(10).std().plot(ax=ax)
        plt.show()
        df.to_csv(ticker)

if __name__ == '__main__':
    get_ticker_std('ADBE')
