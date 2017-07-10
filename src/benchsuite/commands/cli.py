#!/usr/bin/env python
# BenchmarkingSuite - Benchmarking Controller
# Copyright 2014-2017 Engineering Ingegneria Informatica S.p.A.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Developed in the ARTIST EU project (www.artist-project.eu) and in the
# CloudPerfect EU project (https://cloudperfect.eu/)

import argparse
import logging
import sys
from datetime import datetime

from prettytable import PrettyTable

from benchsuite.commands.argument_parser import get_options_parser
from benchsuite.controller import BenchmarkingController
from benchsuite.core.model.exception import BashCommandExecutionFailedException

RUNTIME_NOT_AVAILABLE_RETURN_CODE = 1


def list_executions_cmd(args):

    table = PrettyTable()
    table.field_names = ["Id", "Benchmark", "Created", "Exec. Env.", "Session"]

    with BenchmarkingController(args.config) as bc:
        execs = bc.list_executions()
        for e in execs:
            created = datetime.fromtimestamp(e.created).strftime('%Y-%m-%d %H:%M:%S')
            table.add_row([e.id, e.test.name, created, e.exec_env, e.session.id])

    print(table.get_string())


def list_sessions_cmd(args):

    table = PrettyTable()
    table.field_names = ["Id", "Type", "Created"]

    with BenchmarkingController(args.config) as bc:
        sessions = bc.list_sessions()
        for s in sessions:
            created = datetime.fromtimestamp(s.created).strftime('%Y-%m-%d %H:%M:%S')
            table.add_row([s.id, s.provider.type, created])

        print(table.get_string())


def destroy_session_cmd(args):
    with BenchmarkingController(args.config) as bc:
        bc.destroy_session(args.id)
        print('Session {0} successfully destroyed'.format(args.id))


def new_session_cmd(args):
    with BenchmarkingController(args.config) as bc:
        e = bc.new_session(args.provider, args.service_type)
        print(e.id)


def new_execution_cmd(args):
    with BenchmarkingController(args.config) as bc:
        e = bc.new_execution(args.session, args.tool, args.workload)
        print(e.id)


def prepare_execution_cmd(args):
    with BenchmarkingController(args.config) as bc:
        bc.prepare_execution(args.id)


def collect_results_cmd(args):
    with BenchmarkingController(args.config) as bc:
        out, err = bc.collect_execution_results(args.id)
        print(str(out))
        print(str(err))


def run_execution_cmd(args):
    with BenchmarkingController(args.config) as bc:
        bc.run_execution(args.id, async=args.async)


def execute_onestep_cmd(args):
    with BenchmarkingController() as bc:
        out, err = bc.execute_onestep(args.provider, args.service_type, args.tool, args.workload)
        print('============ STDOUT ============')
        print(out)
        print('============ STDERR ============')
        print(err)

#
#
# def get_options_parser():
#     # create the top-level parser
#     parser = argparse.ArgumentParser(prog='PROG')
#     parser.add_argument('--verbose', '-v', action='count', help='print more information (3 levels)')
#     parser.add_argument('--config', '-c', type=str, help='foo help')
#     subparsers = parser.add_subparsers(help='sub-command help')
#
#
#     # create the parser for the "a" command
#     # new-session --provider-conf [name] --service-type [name]
#     parser_a = subparsers.add_parser('new-session', help='create-env help')
#     parser_a.add_argument('--provider', type=str, help='bar help')
#     parser_a.add_argument('--service-type', type=str, help='bar help')
#     parser_a.set_defaults(func=new_session_cmd)
#
#     parser_a = subparsers.add_parser('list-sessions', help='a help')
#     parser_a.set_defaults(func=list_sessions_cmd)
#
#     parser_a = subparsers.add_parser('destroy-session', help='a help')
#     parser_a.add_argument('id', type=str, help='bar help')
#     parser_a.set_defaults(func=destroy_session_cmd)
#
#     parser_a = subparsers.add_parser('new-exec', help='a help')
#     parser_a.add_argument('session', type=str, help='bar help')
#     parser_a.add_argument('tool', type=str, help='bar help')
#     parser_a.add_argument('workload', type=str, help='bar help')
#     parser_a.set_defaults(func=new_execution_cmd)
#
#     parser_a = subparsers.add_parser('prepare-exec', help='a help')
#     parser_a.add_argument('id', type=str, help='bar help')
#     parser_a.set_defaults(func=prepare_execution_cmd)
#
#     parser_a = subparsers.add_parser('run-exec', help='a help')
#     parser_a.add_argument('id', type=str, help='bar help')
#     parser_a.add_argument('--async', action='store_true', help='bar help')
#     parser_a.set_defaults(func=run_execution_cmd)
#
#
#     parser_a = subparsers.add_parser('list-execs', help='lists the executions')
#     parser_a.set_defaults(func=list_executions_cmd)
#
#     parser_a = subparsers.add_parser('collect-exec', help='collects the outputs of an execution')
#     parser_a.add_argument('id', type=str, help='the execution id')
#     parser_a.set_defaults(func=collect_results_cmd)
#
#
#     parser_a = subparsers.add_parser('exec', help='create-env help')
#     parser_a.add_argument('--provider', type=str, help='bar help')
#     parser_a.add_argument('--service-type', type=str, help='bar help')
#     parser_a.add_argument('--tool', type=str, help='bar help')
#     parser_a.add_argument('--workload', type=str, help='bar help')
#     parser_a.set_defaults(func=execute_onestep_cmd)
#
#     return parser



def main():
    cmds_mapping = {
        'new_session_cmd': None,
        'list_sessions_cmd': None,
        'destroy_session_cmd': None,
        'destroy_session_cmd': None,
        'new_execution_cmd': None,
        'prepare_execution_cmd': None,
        'run_execution_cmd': None,
        'collect_results_cmd': None,
        'execute_onestep_cmd': None,
        'list_executions_cmd': list_executions_cmd
    }

    parser = get_options_parser(cmds_mapping=cmds_mapping)

    args = parser.parse_args(args = sys.argv[1:])

    if not args.verbose:
        args.verbose = 0

    logging_level = logging.ERROR
    logging_format = '%(message)s'

    bench_suite_loggers = logging.getLogger('benchsuite')

    if args.verbose == 1:
        logging_level = logging.INFO
    if args.verbose > 1:
        logging_level = logging.DEBUG
        logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    logging.basicConfig(
        level=logging.CRITICAL,
        stream=sys.stdout,
        format=logging_format)

    bench_suite_loggers.setLevel(logging_level)

    if args.verbose > 2:
        logging.root.setLevel(logging.DEBUG)

    try:
        args.func(args)
    except BashCommandExecutionFailedException as e:
        print(str(e))
        error_file = 'last_cmd_error.dump'
        with open(error_file, "w") as text_file:
            text_file.write("========== CMD ==========\n")
            text_file.write(e.cmd)
            text_file.write('\n\n>>> Exit status was {0}\n'.format(e.exit_status))
            text_file.write("\n\n========== STDOUT ==========\n")
            text_file.write(e.stdout)
            text_file.write("\n\n========== STDERR ==========\n")
            text_file.write(e.stderr)

        print('Command stdout and stderr have been dumped to {0}'.format(error_file))

if __name__ == '__main__':
    main(sys.argv[1:])