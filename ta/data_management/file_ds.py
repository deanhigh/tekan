from pandas import DataFrame

from ta.mdl import DataSource

class FileSource(DataSource):
    def __init__(self, id, filename):
        super(FileSource, self).__init__(id)
        self.filename = filename

    def load(self):
        self.data_frame = DataFrame.from_csv(self.filename)

    def save(self, filename=None):
        return self.data_frame.to_csv(filename if filename else self.filename)