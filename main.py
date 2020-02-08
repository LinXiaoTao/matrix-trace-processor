import argparse
import os
import sys
from collections import defaultdict

from device.device import pull_last_trace, pull_all_traces, pull_n_traces
from importer.interpreter import TraceFileInterpreter
from importer.trace_file import TraceFile
from symbols.mapping_symbols import extract_mapping_symbols


def pull_traces(args):
    if args.last:
        pull_last_trace(args.package)
    elif args.all:
        pull_all_traces(args.package)
    else:
        pull_n_traces(args.package, args.count)
    return


def workflow_traces(args):
    # Make sure the trace file exists
    if not os.path.exists(args.trace):
        print(args.trace, "no such file or directory")
        sys.exit(2)

    if not os.path.exists(args.methodMapping):
        print('{methodMapping}: no such file'.format(methodMapping=args.methodMapping))
        sys.exit(2)

    symbols = extract_mapping_symbols(args.methodMapping)
    tracefile = TraceFile.from_file(args.trace)
    interpreter = TraceFileInterpreter(tracefile, symbols)
    trace = interpreter.interpret()

    stacks = defaultdict(int)  # [frame] -> int (count)
    traversal(trace, stacks)

    # DTrace collapser ignores the first three lines
    print("\n\n\n")
    for k, v in stacks.items():
        for frame in k:
            if str(frame).isdigit():
                print("_", frame, sep='')
            else:
                print(frame, sep='')
        print(v)
        print("\n")


def traversal(trace, stacks):
    stack = []
    index = 0
    while index < len(trace):
        if len(stack) == 0:
            stack.append(trace[index])
        else:
            cur = trace[index]
            last = stack[len(stack) - 1]
            depth = last['depth']
            if depth < cur['depth']:
                stack.append(cur)
            else:
                result = []
                for item in stack:
                    result.append('%s(%sms)' % (item['method'], item['durtime']))
                result.reverse()
                stacks[tuple(result)] = 1
                while len(stack) > 0 and stack[len(stack) - 1]['depth'] >= cur['depth']:
                    stack.pop()
                stack.append(cur)
        index = index + 1
    if len(stack) > 0:
        result = []
        for item in stack:
            result.append('%s(%sms)' % (item['method'], item['durtime']))
        result.reverse()
        stacks[tuple(result)] = 1
    return


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description="Matrix commandline utility!")
    subparsers = parse.add_subparsers(help='Supported features')

    pull_traces_parser = subparsers.add_parser('pull_traces', help='Pull traces from the device')
    pull_traces_parser.set_defaults(func=pull_traces)
    pull_traces_group = pull_traces_parser.add_mutually_exclusive_group(required=True)
    pull_traces_group.add_argument('--last', action='store_true', help='Pull only the last trace')
    pull_traces_group.add_argument("--all", action="store_true", help="Pull all existing traces")
    pull_traces_group.add_argument("--count", type=int, help="Pull the last COUNT traces")
    pull_traces_parser.add_argument('package', type=str, help='Specify the package name using Matrix, e.g. com.foo.bar')

    workflow_traces_parser = subparsers.add_parser('workflow_traces', help='Processing analysis traces')
    workflow_traces_parser.add_argument('trace', type=str, help='Path to downloaded trace')
    workflow_traces_parser.add_argument('methodMapping', type=str, help='methodMapping')
    workflow_traces_parser.set_defaults(func=workflow_traces)

    args = parse.parse_args()
    args.func(args)
