from logging import info


class DataSet(object):
    def __init__(self, id):
        self.id = id
        self.__data_frame = None

    def __get_data_frame(self):
        if self.__data_frame is None and hasattr(self,'load'):
            self.load()
        return self.__data_frame

    def __set_data_frame(self, df):
        self.__data_frame = df

    def get_series(self, series):
        # self.data_frame = 0
        pass

    def __len__(self):
        return self.__get_data_frame().size

    data_frame = property(__get_data_frame, __set_data_frame)


class DataSource(DataSet):
    def load(self):
        pass

    def save(self):
        pass


class Predicate(object):

    def apply(self):
        pass

