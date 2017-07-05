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
from flask_restplus import Api, fields

from benchsuite.model.exception import ControllerConfigurationException, BashCommandExecutionFailedException

blueprint = Blueprint('apiv1', __name__, url_prefix='/api/v1')


description = '''
![Image](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADgAAAA1CAYAAAAUGCjAAAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH4QUYDTQaAhELWQAAAuFJREFUaN7t2k1PGkEYB/D/CixkbevF9tL0I7QnLr5wUrzIelBRAk0PjV4akwab9Ip8APeiadK0EhJsm1qQVvRgQGM0mLQfoumll7Y0TRsW3GU7PZQQ0UVAmdkN2Sd5LuQZ4Me87MwEjhBC0MXRgy4PC2gBLaAFtIDMgEtLS+A4rqMZj8dr76+qKqbHx3XrVlZWLgW0t9tgEcCTK/6qGoDHggDZ7UYgEPj/mqbhgd+PXwcH+AzAeap+GUChUGADRAdx73d34XK5oGka7k9N4Xs2i5eyDL6Dn2c3Ay40OYkfuVzHcUyBejhVVTEjivhzdEQFx2wVNQrHBGgkjvoQbYTziyKKDHBUe7AZ7gUDHDWgHk5RFOa4todoX18fogCkFmp9AwP4sLMDp9MJRVEwI4qo5PNYk2Wmz6a2ejAcDoMQ0lJmcrkazu/zoZLP41mxyHxnQX0VnZ2YwN/jY0NwTIAulwsnhMComy3qwPVUCv1jY3goCDjppuPSjChCVVXYbDYkkknc8noxLwhQzN6DiwC+NskvAH7v7WH2FHI9lcJNrxdzjJFUhqgDwPNSCfLh4Tlk/+goUyS1OdgI+WpzkymS6iLTCJlIJnHd42GCpL6K6iEdDgc2MhlcY4Bkch5shHxXRdJcXa8MXAZw+0ze4TgsCAIqLSJ7PR4s9PbW1ZuqByORSN0+tFQuozI0hEdnvvRFSPvw8Ll60w5RnueR3N5Gz+Bgy8iNrS3YdOpNOwd5nsebdBofHQ681ZmTq6USDvf3kUgkavWv02l80qk35ZWFpmmYC4VwT1EwrXMgfioIcLvdCAaDdfV3derNd6KvXuR+q17kOpuc9i+qNxx4A0A0Gq3baNvtdvzMZrFmMK4jQ3S+mudClpve09DGMXvQG4VjAjQSRx1oNI4q0Aw4eo8Jk+AAAKSNkCSJAGgpfSMjpFwu19rGYrGW2+qlJEnkMsFZ/1WzgBbQAlpAC2gBuzf+AYAvoMr+fMcXAAAAAElFTkSuQmCC)
This is an API to access the Benchmarking Suite

# Benchmarking Suite Model
There are three main concepts in the Benchmarking Suite:
- the **Service Provider**
- the **sessions**
- the **executions**
- and the *benchmarks*

Each BenchmarkingSession has **one** ServiceProvider and **one or more** BenchmarkExecutions
Each BenchmarkExecution has an ExecutionEnvironment and one Benchmark

When the _prepare_ operation is invoked on a BenchmarkExecution, the execution environment is prepared (if it is not exists yet, a new one is requested to the Provider). Then the install commands for the execution BenchmarkTest are executed
 
![image](https://yuml.me/diagram/scruffy/class/[BenchmarkingSession]->[ServiceProvider], [BenchmarkingSession]<>->[BenchmarkExecution])

'''

api = Api(
    blueprint,
    title='Benchmarking Suite REST API',
    version='1.0',
    description=description,
    # All API metadatas
)

bash_command_failed_model = api.model('BashCommandExecutionFailed', {
    'message': fields.String,
    'stdout': fields.String(example='This will be the command stdout'),
    'stderr': fields.String(example='This will be the command stderr')
})

@api.errorhandler(ControllerConfigurationException)
def handle_custom_exception(error):
    return {'message': str(error)}, 400


@api.errorhandler(BashCommandExecutionFailedException)
def handle_command_failed_exception(error):
    return {'message': str(error), 'stdout': str(error.stdout), 'stderr': str(error.stderr)}, 400





from .executions import api as executions_ns
from .sessions import api as sessions_ns

api.add_namespace(sessions_ns)
api.add_namespace(executions_ns)
#api.add_namespace(benchmarks_ns)

