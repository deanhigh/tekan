from functools import reduce

from indicators.kpi import SMA, STDDEV, EWMA, ATR, ATRP, ADX, CCI


def get_all_indicators_df(ticker_source, ind=(STDDEV, SMA, EWMA, ATR, ATRP, ADX, CCI)):
    return reduce(lambda df, ndf: df.join(ndf.create(ticker_source).calc()), ind, ticker_source.underlying_df())

