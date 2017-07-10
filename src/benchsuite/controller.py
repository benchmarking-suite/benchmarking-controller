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

import logging
import os

from appdirs import user_data_dir
from benchsuite.core.model.exception import ControllerConfigurationException, UndefinedExecutionException
from benchsuite.core.model.provider import load_service_provider_from_config_file
from benchsuite.core.model.session import BenchmarkingSession
from typing import Dict

from benchsuite.core.model.benchmark import load_benchmark_from_config_file
from benchsuite.core.model.execution import BenchmarkExecution
from benchsuite.persistence.session import SessionStorageManager

CONFIG_FOLDER_VARIABLE_NAME = 'BENCHSUITE_CONFIG_FOLDER'
STORAGE_FOLDER_VARIABLE_NAME = 'BENCHSUITE_STORAGE_FOLDER'


logger = logging.getLogger(__name__)


class ControllerConfiguration():

    CLOUD_PROVIDERS_DIR = 'providers'
    BENCHMARKS_DIR = 'benchmarks'

    def __init__(self, config_folder):
        self.root = config_folder

    def get_default_data_dir(self):
        d = user_data_dir('BenchmarkingSuite', None)
        if not os.path.exists(d):
            os.makedirs(d)
        return d

    def get_provider_config_file(self, name):
        return self.root + os.path.sep + self.CLOUD_PROVIDERS_DIR + os.path.sep + name + '.conf'

    def get_benchmark_config_file(self, name):
        return self.root + os.path.sep + self.BENCHMARKS_DIR + os.path.sep + name + '.conf'


class BenchmarkingController():
    """
    The main class to control the benchmarking
    """

    def __init__(self, config_folder=None, storage_dir=None):

        if config_folder:
            self.config_folder = config_folder
        else:
            if not CONFIG_FOLDER_VARIABLE_NAME in os.environ:
                raise ControllerConfigurationException(CONFIG_FOLDER_VARIABLE_NAME + ' variable not set')
            else:
                self.config_folder = os.environ[CONFIG_FOLDER_VARIABLE_NAME]

        logger.info('Using config directory at ' + self.config_folder)
        self.configuration = ControllerConfiguration(self.config_folder)
        self.storage_folder = storage_dir or self.configuration.get_default_data_dir()
        self.session_storage = SessionStorageManager(self.storage_folder)
        self.session_storage.load()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.session_storage.store()
        return exc_type is None

    def list_sessions(self) -> Dict[str, BenchmarkingSession]:
        """
        Lists the sessions
        :return: Session list
        """
        return self.session_storage.list()

    def list_executions(self):
        return [item for sublist in self.list_sessions() for item in sublist.list_executions()]

    def get_session(self, session_id: str) -> BenchmarkingSession:
        return self.session_storage.get(session_id)

    def new_session(self, cloud_provider_name: str, cloud_service_name: str) -> BenchmarkingSession:
        c = self.configuration.get_provider_config_file(cloud_provider_name)
        p = load_service_provider_from_config_file(c, cloud_service_name)
        s = BenchmarkingSession(p)
        self.session_storage.add(s)
        return s

    def destroy_session(self, session_id: str) -> None:
        s = self.get_session(session_id)
        logger.debug('Session loaded: {0}'.format(s))
        s.destroy()
        self.session_storage.remove(s)

    def get_execution(self, exec_id, session_id=None):
        if session_id:
            return self.session_storage.get(session_id).get_execution(exec_id)

        for s in self.session_storage.list():
            try:
                return s.get_execution(exec_id)
            except:
                pass

        raise UndefinedExecutionException('Execution with id={0} does not exist'.format(exec_id))

    def new_execution(self, session_id: str, tool: str, workload: str) -> BenchmarkExecution:
        s = self.session_storage.get(session_id)
        config_file = self.configuration.get_benchmark_config_file(tool)
        b = load_benchmark_from_config_file(config_file, workload)
        e = s.new_execution(b)
        return e

    def prepare_execution(self, exec_id, session_id=None):
        e = self.get_execution(exec_id, session_id)
        logger.debug("Execution loaded: {0}".format(e))
        e.prepare()

    def run_execution(self, exec_id, async=False, session_id=None):
        e = self.get_execution(exec_id, session_id)
        e.execute(async=async)


    def collect_execution_results(self, exec_id, session_id=None):
        e = self.get_execution(exec_id, session_id)
        return e.collect_result()


    def execute_onestep(self, provider, service_type: str, tool: str, workload: str) -> str:
        session = self.new_session(provider, service_type)
        execution = self.new_execution(session.id, tool, workload)
        execution.prepare()
        execution.execute()
        out, err = execution.collect_result()
        session.destroy()
        return out, err