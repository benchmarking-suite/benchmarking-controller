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
import os

import sys

from org.benchsuite.controller import BenchmarkingController, CONFIG_FOLDER_VARIABLE_NAME
from org.benchsuite.util import print_message, set_output_stream, set_output_verbosity
from prettytable import PrettyTable

RUNTIME_NOT_AVAILABLE_RETURN_CODE = 1



def list_executions_cmd(args):

    table = PrettyTable()
    table.field_names = ["Id", "Type"]

    with BenchmarkingController(args.config) as bc:
        execs = bc.list_executions()
        for e in execs:
            table.add_row([e.id, ''])

    print_message(table.get_string())

def list_sessions_cmd(args):

    table = PrettyTable()
    table.field_names = ["Id", "Type"]

    with BenchmarkingController(args.config) as bc:
        sessions = bc.list_sessions()
        for s in sessions:
            table.add_row([s.id, s.provider.type])

    print_message(table.get_string())


def destroy_session_cmd(args):
    with BenchmarkingController(args.config) as bc:
        bc.destroy_session(args.id)


def new_session_cmd(args):
    with BenchmarkingController(args.config) as bc:
        e = bc.new_session(args.provider, args.service_type)
        print_message(e.id)

def new_execution_cmd(args):
    with BenchmarkingController(args.config) as bc:
        e = bc.new_execution(args.session, args.tool, args.workload)
        print_message(e.id)


def prepare_execution_cmd(args):
    with BenchmarkingController(args.config) as bc:
        bc.prepare_execution(args.id)


def run_execution_cmd(args):
    with BenchmarkingController(args.config) as bc:
        bc.run_execution(args.id, async=args.async)


def execute_onestep_cmd(args):
    with BenchmarkingController() as bc:
        eid = bc.execute_onestep(args.provider_conf, args.service, args.tool)
        print_message(eid)

#
# def list_environment_cmd(args):
#
#     table = PrettyTable()
#     table.field_names = ["Id", "Type", "VMs"]
#
#     with BenchmarkingController(args.config) as bc:
#         envs = bc.list_environments()
#         for id, e in envs.items():
#             table.add_row([id, e.type, len(e.vms_pool)])
#
#     print_message(table.get_string())

#
# def get_test_runtime_cmd(args):
#     test_id = args.id
#     phase = args.phase or 'run'
#
#     with BenchmarkingController(args.config) as bc:
#         t = bc.get_test_runtime(test_id, phase)
#         if t:
#             print_message(t)
#         else:
#             sys.exit(RUNTIME_NOT_AVAILABLE_RETURN_CODE)
#
#
# def list_tests_cmd(args):
#     with BenchmarkingController(args.config) as bc:
#         tests = bc.list_executions()
#         for id, e in tests.items():
#             print(id + ' :' + str(e))
#
#
#
# def destroy_environment_cmd(args):
#     with BenchmarkingController(args.config) as bc:
#         eid = bc.destroy_environment(args.id)
#         print_message('Environment {0} successfully destoryed'.format(eid), verbosity=2)
#
#
# def create_new_execution_cmd(args):
#     with BenchmarkingController(args.config) as bc:
#         e = bc.create_new_execution(args.env_id, args.tool, args.workload)
#         print(e.id)
#
#
#
#
#
# def collect_execution_cmd(args):
#     with BenchmarkingController(args.config) as bc:
#         bc.collect_results(args.id)
#

def main(cmdline_args):
    # create the top-level parser
    parser = argparse.ArgumentParser(prog='PROG')
    parser.add_argument('--foo', action='store_true', help='foo help')
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--config', '-c', type=str, help='foo help')
    subparsers = parser.add_subparsers(help='sub-command help')

    # create the parser for the "a" command
    # new-session --provider-conf [name] --service-type [name]
    parser_a = subparsers.add_parser('new-session', help='create-env help')
    parser_a.add_argument('--provider', type=str, help='bar help')
    parser_a.add_argument('--service-type', type=str, help='bar help')
    parser_a.set_defaults(func=new_session_cmd)

    parser_a = subparsers.add_parser('list-sessions', help='a help')
    parser_a.set_defaults(func=list_sessions_cmd)

    parser_a = subparsers.add_parser('destroy-session', help='a help')
    parser_a.add_argument('id', type=str, help='bar help')
    parser_a.set_defaults(func=destroy_session_cmd)

    parser_a = subparsers.add_parser('new-exec', help='a help')
    parser_a.add_argument('session', type=str, help='bar help')
    parser_a.add_argument('tool', type=str, help='bar help')
    parser_a.add_argument('workload', type=str, help='bar help')
    parser_a.set_defaults(func=new_execution_cmd)

    parser_a = subparsers.add_parser('prepare-exec', help='a help')
    parser_a.add_argument('id', type=str, help='bar help')
    parser_a.set_defaults(func=prepare_execution_cmd)

    parser_a = subparsers.add_parser('run-exec', help='a help')
    parser_a.add_argument('id', type=str, help='bar help')
    parser_a.add_argument('--async', action='store_true', help='bar help')
    parser_a.set_defaults(func=run_execution_cmd)


    parser_a = subparsers.add_parser('list-exec', help='a help')
    parser_a.set_defaults(func=list_executions_cmd)


    os.environ[CONFIG_FOLDER_VARIABLE_NAME] = '/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig'

    args = parser.parse_args(cmdline_args)


    set_output_stream(sys.stdout)
    set_output_verbosity(args.verbose or 0)

    args.func(args)


if __name__ == '__main__':

    main(sys.argv[1:])


    # parser_a = subparsers.add_parser('execute', help='a help')
    # parser_a.add_argument('--provider', type=str, help='bar help')
    # parser_a.add_argument('--service-type', type=str, help='bar help')
    # parser_a.add_argument('executions', type=str, nargs='*', help='bar help')
    # parser_a.set_defaults(func=execute_onestep_cmd)


    # parser_a = subparsers.add_parser('collect-test', help='a help')
    # parser_a.add_argument('id', type=str, help='bar help')
    # parser_a.set_defaults(func=collect_execution_cmd)
    #
    # parser_a = subparsers.add_parser('get-test-runtime', help='a help')
    # parser_a.add_argument('id', type=str, help='bar help')
    # parser_a.add_argument('--phase', type=str, help='bar help')
    # parser_a.set_defaults(func=get_test_runtime_cmd)








    # args = parser.parse_args(
    #     'execute '
    #     '--provider-conf /home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/cloud_providers/filab-vicenza.conf '
    #     '--service ubuntu_small '
    #     'cfd workload1'.split())


    # args = parser.parse_args(
    #     'new-session --provider filab-vicenza --service centos_medium'.split())

    # args = parser.parse_args(
    #     'new-exec 39e13bdd-5d72-11e7-8a4f-9c4e36dc7538 filebench Workload19'.split())

    # args = parser.parse_args(
    #     '-vv prepare-exec 570d8a9e-5d72-11e7-8a4f-9c4e36dc7538'.split())


    # args = parser.parse_args(
    #     'create-test idle --workload idle30 --env-id 47f9b2dc-5c0d-11e7-b64e-742b62857160'.split())


    # args = parser.parse_args(
    #     'get-test-runtime 60672912-5c0d-11e7-b64e-742b62857160'.split())

    # args = parser.parse_args(
    #     'start-test 7c540d74-5a79-11e7-b915-742b62857160'.split())

    # args = parser.parse_args(
    #     'get-test-runtime --phase run 8040aada-5b48-11e7-bfdc-9c4e36dc7538'.split())


    # args = parser.parse_args(
    #     '-vv list-sessions'.split())

    # args = parser.parse_args(
    #     '-vv destroy-session 27694389-5d6c-11e7-8a4f-9c4e36dc7538'.split())



