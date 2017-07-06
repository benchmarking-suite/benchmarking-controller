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
import os

import logging

import sys

from benchsuite.controller import CONFIG_FOLDER_VARIABLE_NAME
from benchsuite.core.model.provider import load_service_provider_from_config_file
from benchsuite.execution.vm_environment import VMSetExecutionEnvironmentRequest, VM

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    os.environ[CONFIG_FOLDER_VARIABLE_NAME] = '/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig'


    s = load_service_provider_from_config_file('/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig/providers/amazon-us-west-1.conf', 'centos_medium')
    #
    # vm = VM('i-08c2f801d03d5d45a', None, None, None, None, None)
    #
    # s.vms_pool = [vm]
    #
    # s.destroy_service()

    s.get_execution_environment(VMSetExecutionEnvironmentRequest(1))
