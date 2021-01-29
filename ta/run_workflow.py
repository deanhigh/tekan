import argparse
from pprint import pprint

from ta.mdl.workflows import WorkflowContext, WorkflowLoader
import ta.data_management
import ta.indicators
import ta.predicates
import ta.functions

if __name__ == '__main__':
    argsp = argparse.ArgumentParser('Run a workflow')
    argsp.add_argument('-f', action='store', dest='workflow_file', default=None , help='Workflow descriptor')
    argsp.add_argument('-i', action='store', dest='indicator', default=None , help='Indicator to output')
    args = argsp.parse_args()

    if args.workflow_file and args.indicator:
        wc = WorkflowContext.load(WorkflowLoader.from_yaml(args.workflow_file))
        pprint(wc.get_data(args.indicator))
    else:
        argsp.print_help()
