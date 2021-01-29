

class DataSet(object):
    def __init__(self, id):
        self.id = id

    def load(self):
        return NotImplemented

    def __str__(self):
        return id


class DataSeriesDataSet(DataSet):
    def __init__(self, id, data_series):
        super(DataSeriesDataSet, self).__init__(id)
        self.__data_series = data_series


class DataFrameDataSet(DataSet):
    def __init__(self, id, series_ids):
        super(DataFrameDataSet, self).__init__(id)
        self.series_ids = series_ids
        self.__data_frame = None

    def get_series(self, series_id):
        return self.data_frame[series_id]

    def series_pointers(self):
        return { i:SeriesPointer(self, i) for i in self.series_ids.values() }

    def __get_data_frame(self):
        if self.__data_frame is None and hasattr(self, 'load'):
            self.load()
        return self.__data_frame

    def __set_data_frame(self, df):
        self.__data_frame = df

    def __len__(self):
        return self.__get_data_frame().size

    data_frame = property(__get_data_frame, __set_data_frame)


class ExportableDataFrameDataSet(object):
    def save(self, filename):
        return self.data_frame.to_csv(filename)


class SeriesPointer(object):
    def __init__(self, data_set, series):
        self.data_set = data_set
        self.series = series

    def get_data(self, wc=None):
        return self.data_set.data_frame[self.series]

    data = property(get_data)


class IndicatorSeriesPointer(object):
    def __init__(self, indicator, series):
        self.indicator = indicator
        self.series = series

    def get_data(self, wc):
        return self.indicator.calc(wc)

class Predicate(object):
    def apply(self):
        pass
