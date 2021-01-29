from pandas import DataFrame, Series


class WorkflowDescriptor(object):
    pass


class WorkflowContext(object):
    def __init__(self):
        self.__ts_data_frame = DataFrame()
        self.__ts_ids = set()

    @classmethod
    def blank(cls):
        """ Create a blank workflow context builder which can be used to programatically build workflows """
        return cls()

    @classmethod
    def from_descriptor(cls, workflow_descriptor):
        """ Create a workflow from a workflow descriptor """
        pass

    def add_ts_data(self, data):
        """ Add pandas series or dataframe to the set, raise DuplicateTimeSeries if series alread exists"""
        columns_to_add = {data.name} if isinstance(data, Series) else {x for x in data.columns.values}
        dupes = self.__ts_ids.intersection(columns_to_add)
        if len(dupes) > 0:
            raise DuplicateTimeSeries(duplicate_columns=dupes)

        self.__ts_data_frame += data
        self.__ts_ids.update(columns_to_add)

    @property
    def ts_ids(self):
        return self.__ts_ids

    @property
    def ts_data_frame(self):
        return self.__ts_data_frame


class DuplicateTimeSeries(Exception):
    def __init__(self, duplicate_columns):
        super(DuplicateTimeSeries, self).__init__("Cannot add duplicate columns to context data frame")
        self.duplicate_columns = duplicate_columns
