from ta.indicators import Indicator, talib, Series


class TR(Indicator):
    def __init__(self, id, low_data_id, high_data_id, close_data_id):
        self.low_data_id = low_data_id
        self.high_data_id = high_data_id
        self.close_data_id = close_data_id
        super(TR, self).__init__(id)

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['id'], kwargs['low_data_id'], kwargs['high_data_id'], kwargs['close_data_id'])

    def calc(self, context):
        low_series = context.get_data(self.low_data_id)
        high_series = context.get_data(self.high_data_id)
        close_series = context.get_data(self.close_data_id)
        return Series(talib.TRANGE(low_series.values, high_series.values, close_series.values), index=low_series.index.values)

# class TR(BaseTrueRange):
#     def calc(self, context):

        # class TR(Indicator):
        #     """ True range """
        #
        #     def _tr(self, vals):
        #         prev_close = vals[CLOSE + '_prev']
        #         m1 = (vals[HIGH] - vals[LOW])
        #         m2 = abs(vals[HIGH] - prev_close)
        #         m3 = abs(vals[LOW] - prev_close)
        #         tr = max(m1, m2, m3) if not math.isnan(prev_close) else None
        #         return tr
        #
        #     def calc(self):
        #         data = self.data_set.underlying_field_df(HIGH). \
        #             join(self.data_set.underlying_field_df(LOW)). \
        #             join(self.data_set.underlying_field_df(CLOSE)). \
        #             join(self.data_set.underlying_field_df(CLOSE).shift(), rsuffix='_prev')
        #         tr = data.apply(self._tr, axis=1).to_frame(name='TR')
        #         return tr
        #
        #
        # class ATR(Indicator):
        #     """ Average True Range """
        #
        #     def calc(self, period=14):
        #         atr = TR.create(self.data_set).calc().rolling(period).apply(Smoothing.smoothing(period)).rename(
        #             columns={'TR': 'ATR{}'.format(period)})
        #         return atr
        #
        #
        # class ATRP(Indicator):
        #     """Average true range as percentage of close"""
        #
        #     def calc(self, period=14):
        #         data = ATR.create(self.data_set).calc(period).join(self.data_set.underlying_field_df(CLOSE))
        #         return data.apply(lambda v: (v['ATR{}'.format(period)] / v[CLOSE]) * 100, axis=1).to_frame(
        #             'ATRP{}'.format(period))
        #
