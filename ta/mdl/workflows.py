import logging

log = logging.getLogger('workflows')

from pprint import pformat
import yaml


def load_workflow_entry(entry, default_cls=None):
    """
    Load a workflow unit based on the class attribute provided, assumes a from_descriptor class method
    Will default to default_cls if no no class attribute found.
    """
    try:
        mod = cls = entry.get('class', default_cls)
        log.debug("Loading workflow entry cls=%s", mod)
        if isinstance(cls, str):
            components = cls.split('.')
            mod = __import__(components[0])
            for comp in components[1:]:
                mod = getattr(mod, comp)
        return mod.from_descriptor(**entry)
    except Exception as e:
        log.error("Failed to parse workflow descriptor yaml\n%s", pformat(entry))
        raise e


class WorkflowLoader(object):
    def __init__(self, sources, indicators, triggers, functions):
        self.sources = sources
        self.indicators = indicators
        self.triggers = triggers
        self.functions = functions

    @classmethod
    def from_yaml(cls, yaml_file):
        with open(yaml_file, 'r') as f:
            return WorkflowLoader.from_dict(yaml.load(f))

    @classmethod
    def from_dict(cls, desc):
        ret = cls({x['id']: load_workflow_entry(x) for x in desc['sources']},
                  {x['id']: load_workflow_entry(x) for x in desc['indicators']},
                  {x['id']: load_workflow_entry(x, 'ta.mdl.Trigger') for x in desc.get('triggers', [])},
                  {x['id']: load_workflow_entry(x) for x in desc.get('functions', [])})
        return ret

    def get_data_pointers(self):
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
        self.__triggers = dict()

    @classmethod
    def load(cls, loader):
        wc = cls()
        wc.__data_sets.update(loader.get_data_pointers())
        wc.__data_sets.update(loader.functions)
        wc.__triggers.update(loader.triggers)
        return wc

    @property
    def datasets(self):
        return self.__data_sets

    @property
    def triggers(self):
        return self.__triggers

    def add_dataset(self, dataset):
        self.datasets[dataset.id] = dataset

    def get_data(self, data_id):
        """
        Gets the identified dataset if it is found. If its not found it will attempt to create using create func.
        """
        return self.datasets[data_id].get_data(self)

    def get_trigger(self, trigger_id):
        return self.triggers[trigger_id]


class DuplicateTimeSeries(Exception):
    def __init__(self, duplicate_columns):
        super(DuplicateTimeSeries, self).__init__("Cannot add duplicate columns to context data frame")
        self.duplicate_columns = duplicate_columns
