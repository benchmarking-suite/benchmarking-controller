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


import configparser
import os
import uuid
from abc import ABC, abstractmethod

import sys

from org.benchsuite.model.exception import ControllerConfigurationException
from org.benchsuite.model.execution import ExecutionEnvironmentRequest, ExecutionEnvironment


class ServiceProvider(ABC):

    @abstractmethod
    def __init__(self, type):
        self.id = str(uuid.uuid1())
        self.type = type

    @abstractmethod
    def get_execution_environment(self, request: ExecutionEnvironmentRequest) -> ExecutionEnvironment:
        pass

    @abstractmethod
    def destroy_service(self):
        pass

    @staticmethod
    @abstractmethod
    def load_from_config_file(config, service_type):
        pass


def load_service_provider_from_config_file(config_file, service_type) -> ServiceProvider:
    if not os.path.isfile(config_file):
        raise ControllerConfigurationException('Config file {0} does not exist'.format(config_file))

    config = configparser.ConfigParser()
    config.read(config_file)


    provider_class = config['provider']['class']

    module_name, class_name = provider_class.rsplit('.', 1)

    __import__(module_name)
    module = sys.modules[module_name]
    clazz = getattr(module, class_name)

    return clazz.load_from_config_file(config, service_type)