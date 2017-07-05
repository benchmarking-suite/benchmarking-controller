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
from benchsuite.controller import BenchmarkingController

from benchsuite.rest.apiv1.executions import execution_model, new_execution_model

api = Namespace('sessions', description='Benchmarking Sessions operations')

api.models[execution_model.name] = execution_model
api.models[new_execution_model.name] = new_execution_model

provider_model = api.model('Provider', {
    'id': fields.String,
    'type': fields.String,
    'image': fields.String,
    'size': fields.String
})

session_model = api.model('Session', {
    'id': fields.String,
    'provider': fields.Nested(provider_model),
    'created': fields.String,
    'executions': fields.String
})

new_session_model = api.model('NewSession', {
    'provider': fields.String,
    'service-type': fields.String
})

@api.route('/')
class SessionList(Resource):

    @api.marshal_with(session_model)
    def get(self):
        with BenchmarkingController() as bc:
            return list(bc.list_sessions())

    @api.expect(new_session_model)
    @api.marshal_with(session_model)
    def post(self):
        with BenchmarkingController() as bc:
            return bc.new_session(self.api.payload['provider'], self.api.payload['service-type'])


@api.route('/<string:session_id>')
class Session(Resource):

    @api.marshal_with(session_model)
    def get(self, session_id):
        with BenchmarkingController() as bc:
            return bc.get_session(session_id)

    def delete(self, session_id):
        with BenchmarkingController() as bc:
            bc.destroy_session(session_id)
        return '', 204


@api.route('/<string:session_id>/executions/')
class SessionExecution(Resource):

    @api.marshal_with(execution_model)
    def get(self, session_id):
        with BenchmarkingController() as bc:
            return list(bc.get_session(session_id).list_executions())


    @api.expect(new_execution_model)
    @api.marshal_with(execution_model, code=200)
    def post(self, session_id):
        with BenchmarkingController() as bc:
            return bc.new_execution(session_id, self.api.payload['tool'], self.api.payload['workload'])