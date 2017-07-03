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

from flask_restplus import Namespace, Resource, fields

from org.benchsuite.controller import BenchmarkingController
from org.benchsuite.model.exception import BashCommandExecutionFailedException
from org.benchsuite.rest.apiv1.benchmarks import benchmark_model

api = Namespace('executions', description='Executions operations')


# register models from the other namespaces
api.models[benchmark_model.name] = benchmark_model


execution_model = api.model('Execution', {
    'id': fields.String,
    'test': fields.Nested(benchmark_model)
})

new_execution_model = api.model('NewExecution', {
    'tool': fields.String,
    'workload': fields.String
})


@api.route('/')
class ExecutionList(Resource):

    @api.marshal_with(execution_model)
    def get(self):
        with BenchmarkingController() as bc:
            return list(bc.list_executions())


@api.route('/<string:exec_id>')
class Execution(Resource):

    @api.marshal_with(execution_model)
    def get(self, exec_id):
        with BenchmarkingController() as bc:
            return bc.get_execution(exec_id)


@api.route('/<string:exec_id>/prepare')
class ExecutionPrepareACtion(Resource):

    @api.errorhandler(BashCommandExecutionFailedException)
    def post(self, exec_id):
        with BenchmarkingController() as bc:
            bc.prepare_execution(exec_id)
            print('ciao')
            return '', 204


@api.route('/<string:exec_id>/run')
class ExecutionRunACtion(Resource):

    def post(self, exec_id):
        with BenchmarkingController() as bc:
            bc.run_execution(exec_id)
            return '', 204