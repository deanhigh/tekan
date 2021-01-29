import yaml



class WorkflowLoader(object):
    def __init__(self, sources, indicators):
        self.sources = sources
        self.indicators = indicators

    @staticmethod
    def load_wf_entry(entry):
        cls = entry['class']
        components = cls.split('.')
        mod = __import__(components[0])
        for comp in components[1:]:
            mod = getattr(mod, comp)
        return mod.from_descriptor(**entry)

    @classmethod
    def from_yaml(cls, yaml_file):
        with open(yaml_file, 'r') as f:
            return WorkflowLoader.from_dict(yaml.load(f))

    @classmethod
    def from_dict(cls, desc):
        ret = cls({x['id']:cls.load_wf_entry(x) for x in desc['sources']},
                  {x['id']:cls.load_wf_entry(x) for x in desc['indicators']})
        return ret

    def get_datasets(self):
        ret = dict()
        for i in self.sources.values():
            ret.update(i.series_pointers())
        for i in self.indicators.values():
            ret.update(i.output_pointers())
        return ret


class WorkflowContext(object):
    """
    The workflow context contains and manages the current running set of data.
    """
    def __init__(self):
        self.__data_sets = dict()
        self.__ = dict()

    @classmethod
    def load(cls, loader):
        wc = cls()
        wc.datasets.update(loader.get_datasets())
        return wc

    def add_dataset(self, dataset):
        self.datasets[dataset.id] = dataset

    def add_indicator(self, indicator):
        self.indicator[indicator.id] = indicator

    def get_or_create_dataset(self, dataset_id, create_func=None):
        """
        Gets the identified dataset if it is found. If its not found it will attempt to create using create func.
        """
        if dataset_id not in self.datasets and create_func:
            self.datasets[dataset_id] = create_func
        return self.datasets[dataset_id]

    def get_data(self, data_id):
        """
        Gets the identified dataset if it is found. If its not found it will attempt to create using create func.
        """
        return self.datasets[data_id].data

    @property
    def datasets(self):
        return self.__data_sets



class DuplicateTimeSeries(Exception):
    def __init__(self, duplicate_columns):
        super(DuplicateTimeSeries, self).__init__("Cannot add duplicate columns to context data frame")
        self.duplicate_columns = duplicate_columns
