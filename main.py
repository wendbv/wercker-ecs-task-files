from collections import OrderedDict
import json
import os
import sys
import re


try:
    basestring = basestring
except NameError:
    # Python 3 has no basestring type
    basestring = str


def get_env_vars(prefix=''):
    return {
        k[len(prefix):]: v
        for k, v in os.environ.items()
        if k.startswith(prefix)
    }


def parse_json(filename):
    with open(filename) as fid:
        return json.load(fid, object_pairs_hook=OrderedDict)


def insert_environment(jsondata, env):
    for item in jsondata:
        item['environment'] = [{'name': k, 'value': v} for k, v in env.items()]


def handle_single_substitution(text):
    if '$' not in text:
        return text

    return re.sub(
        r'\$([a-zA-Z_]+)',
        lambda match: os.environ.get(match.group(1), match.group(0)),
        text
    )


def handle_substitutions(jsondata):
    if isinstance(jsondata, list):
        lst = enumerate(jsondata)
    elif isinstance(jsondata, dict):
        lst = jsondata.items()
    else:
        return

    for k, v in lst:
        if isinstance(v, basestring):
            jsondata[k] = handle_single_substitution(v)
        else:
            handle_substitutions(v)


def write_json(jsondata, fid, terse=False):
    if terse:
        json.dump(fid, jsondata, separators=(',', ':'))
    else:
        json.dump(fid, jsondata, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Put environment variables into a task definition')

    parser.add_argument(
        'taskfile',
        help='Taskfile to use as input')

    parser.add_argument(
        '--prefix',
        default='ECS_',
        help='Only process environment variables with this prefix')

    parser.add_argument(
        '-v', '--verbose',
        help='Be more verbose',
        default=False,
        action='store_true'
    )

    parser.add_argument(
        '-t', '--terse',
        help='Write compact json',
        default=False,
        action='store_true'
    )

    parser.add_argument(
        'output',
        help='Taskfile to write to',
        default='-',
        nargs='?')

    args = parser.parse_args()

    env = get_env_vars(args.prefix)

    if args.verbose:
        for item in env.items():
            sys.stderr.write(' = '.join(item))
            sys.stderr.write('\n')

    jsondata = parse_json(args.taskfile)

    handle_substitutions(jsondata)

    insert_environment(jsondata, env)

    if args.output == '-':
        args.output = sys.stdout
    else:
        args.output = open(args.output, 'w')

    try:
        write_json(args.output, jsondata, args.terse)
    finally:
        args.output.close()
