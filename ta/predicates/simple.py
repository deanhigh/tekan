from ta.mdl import Predicate
import logging

log = logging.getLogger('predicates')


def handle_input(input):
    if isinstance(input, dict):
        return input['function']
    else:
        return input


class Expression(Predicate):
    def __init__(self, expression, input, value = None):
        self.expression = expression
        self.input = handle_input(input)
        self.value = value

    def apply(self, context):
        params = {'value': self.value, 'input': context.get_data(self.input)}
        log.debug("Applying predicate %s %s", self.expression, params)
        return eval(self.expression, params)

    @classmethod
    def from_descriptor(cls, **kwargs):
        return cls(kwargs['expression'], kwargs['input'], kwargs['value'])

