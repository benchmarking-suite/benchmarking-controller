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


from flask import Blueprint
from flask_restplus import Api

from org.benchsuite.model.exception import ControllerConfigurationException, BashCommandExecutionFailedException
from .sessions import api as sessions_ns
from .executions import api as executions_ns
from .benchmarks import api as benchmarks_ns

blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')


description = '''
This is an API to access the Benchmarking Suite

# Model
[image](https://yuml.me/diagram/scruffy/class/[BenchmarkingSession]->[ServiceProvider], [BenchmarkingSession]<>->[BenchmarkExecution])

~~~

     ┌───┐          ┌─────┐
     │Bob│          │alice│
     └─┬─┘          └──┬──┘
       │    hello      │   
       │───────────────│   
     ┌─┴─┐          ┌──┴──┐
     │Bob│          │alice│
     └───┘          └─────┘


~~~

'''

api = Api(
    blueprint,
    title='My Title',
    version='1.0',
    description=description,
    # All API metadatas
)

api.add_namespace(sessions_ns)
api.add_namespace(executions_ns)
api.add_namespace(benchmarks_ns)


@api.errorhandler(ControllerConfigurationException)
def handle_custom_exception(error):
    return {'message': str(error)}, 400


@api.errorhandler(BashCommandExecutionFailedException)
def handle_command_failed_exception(error):
    return {'message': str(error), 'stdout': str(error.stdout), 'stderr': str(error.stderr)}, 400