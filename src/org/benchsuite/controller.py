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

from appdirs import user_data_dir
from typing import Dict

from org.benchsuite.model.benchmark import load_benchmark_from_config_file
from org.benchsuite.model.exception import ControllerConfigurationException, UndefinedExecutionException
from org.benchsuite.model.execution import BenchmarkExecution
from org.benchsuite.model.provider import load_service_provider_from_config_file
from org.benchsuite.model.session import BenchmarkingSession
from org.benchsuite.persistence.session import SessionStorageManager
from org.benchsuite.util import print_message

CONFIG_FOLDER_VARIABLE_NAME = 'BENCHSUITE_CONFIG_FOLDER'
STORAGE_FOLDER_VARIABLE_NAME = 'BENCHSUITE_STORAGE_FOLDER'


class ControllerConfiguration():

    CLOUD_PROVIDERS_DIR = 'cloud_providers'
    BENCHMARKS_DIR = 'tests'

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

    def __init__(self, config_folder=None, storage_dir=None):

        if config_folder:
            self.config_folder = config_folder
        else:
            if not CONFIG_FOLDER_VARIABLE_NAME in os.environ:
                raise ControllerConfigurationException(CONFIG_FOLDER_VARIABLE_NAME + ' variable not set')
            else:
                self.config_folder = os.environ[CONFIG_FOLDER_VARIABLE_NAME]

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
        e.prepare()

    def run_execution(self, exec_id, async=False, session_id=None):
        e = self.get_execution(exec_id, session_id)
        e.execute(async=async)


    def collect_execution_results(self, exec_id, session_id=None):
        e = self.get_execution(exec_id, session_id)
        return e.collect_result()


    # def create_new_execution(self, env_id, tool, workload):
    #     r = env_manager.get(env_id)
    #     t = BenchmarkingTest(tool, workload)
    #     e = exec_manager.create_new_execution(r.id, t)
    #     return e

    #
    # def create_new_environment_by_name(self, cloud_provider_name, cloud_service_name):
    #     c = self.configuration.get_cloud_provider_config(cloud_provider_name)
    #     return self.create_new_environment(c, cloud_service_name)


    # def create_new_environment(self, cloud_provider_conf, cloud_service_name):
    #
    #     # r = SimpleTargetEnvironmentManager(
    #     #     [VM('217.172.12.215', 'ubuntu', '/home/ggiammat/credentials/filab-vicenza/ggiammat-key.pem')])
    #
    #     cloud_service = get_cloud_service(cloud_provider_conf, cloud_service_name)
    #
    #     e = env_manager.create_new_libcloud_environment(cloud_service)
    #
    #     #e.clean_up()
    #
    #     return e

    # def get_test_runtime(self, exec_id, phase):
    #     e = exec_manager.get(exec_id)
    #     e.get_runtime(phase)

    # def list_environments(self):
    #     return env_manager.list()

    # def list_executions(self):
    #     return exec_manager.list()

    # def destroy_environment(self, env_id):
    #     e = env_manager.get(env_id)
    #     e.clean_up()
    #     env_manager.delete(env_id)
    #
    #
    # def get_environment(self, env_id):
    #     return env_manager.get(env_id)



    #
    #
    # def collect_results(self, exec_id):
    #     e = exec_manager.get(exec_id)
    #     e.get_result()
    #
    # def execute_onestep(self, cloud_provider_conf, cloud_service_name, tool):
    #     env = self.create_new_environment(cloud_provider_conf, cloud_service_name)
    #
    #     executions = []
    #
    #     for i in range(0, len(tool), 2):
    #         exec = self.create_new_execution(env.id, tool[i], tool[i+1])
    #         self.prepare_execution(exec.id)
    #         self.start_execution(exec.id, async=False)
    #         self.collect_results(exec.id)
    #         executions.append(exec.id)
    #
    #     self.destroy_environment(env.id)
    #     return executions

    # def close(self):
    #     exec_manager.store()
    #     env_manager.store()
