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
import time
from configparser import ConfigParser

from libcloud.compute.providers import get_driver
from benchsuite.execution.vm_environment import VMSetExecutionEnvironment, VM
from benchsuite.model.execution import ExecutionEnvironmentRequest, ExecutionEnvironment
from benchsuite.util import run_ssh_cmd

from benchsuite.model.provider import ServiceProvider

logger = logging.getLogger(__name__)

class LibcloudComputeProvider(ServiceProvider):


    def __init__(self, type, endpoint, access_id, secret_key):
        super().__init__('libcloud')
        self.libcloud_type = type
        self.endpoint = endpoint
        self.access_id = access_id
        self.secret_key = secret_key
        self.extra_params = None
        self.image = None
        self.size = None
        self.key_name = None
        self.key_path = None
        self.vm_user = None
        self.platform = None
        self.working_dir = None
        self.post_create_script = 'echo "Hello World!"'
        self.vms_pool = []

    def get_execution_environment(self, request: ExecutionEnvironmentRequest) -> ExecutionEnvironment:
        if len(self.vms_pool) < request.n_vms:
            for i in range(request.n_vms - len(self.vms_pool)):
                self.vms_pool.append(self.__create_vm())

        return VMSetExecutionEnvironment(self.vms_pool[:request.n_vms])

    def destroy_service(self):
        driver = self.__get_libcloud_drv()
        nodes_id = [v.id for v in self.vms_pool]
        to_delete = [n for n in driver.list_nodes() if n.id in nodes_id]
        logger.info('{0} nodes to delete'.format(len(to_delete)))
        for n in to_delete:
            logger.info('Deleting node ' + n.id)
            n.destroy()

    def __get_libcloud_drv(self):
        drv = get_driver(self.libcloud_type)
        driver = drv(self.access_id, self.secret_key, ex_force_auth_url=self.endpoint, **self.extra_params)
        return driver

    def __create_vm(self):

        #1. get the driver
        driver = self.__get_libcloud_drv()

        #2. select the correct image and size
        sizes = driver.list_sizes()
        images = driver.list_images()
        size = [s for s in sizes if s.name == self.size][0]
        image = [i for i in images if i.name == self.image][0]

        logger.debug('Creating new Instance with image %s and size %s', image.name, size.name)
        #3. create the node and wait until RUNNING
        node = driver.create_node(name='test node', image=image, size=size, ex_keyname=self.key_name)
        driver.wait_until_running([node], wait_period=10)

        #4. refresh the info of the node
        node = [i for i in driver.list_nodes() if i.uuid == node.uuid][0]

        logger.debug('New Instance created with node_id=%s', node.id)

        #5. try to assign a free public ip
        if not node.public_ips:
            p_ip = self.__get_available_public_ip(driver)
            if p_ip:
                logger.debug('Trying to assign the public ip %s to the new instance', p_ip)
                driver.ex_attach_floating_ip_to_node(node, p_ip)
            else:
                logger.warning('No floating public ips available!')


        while not node.public_ips:
            time.sleep(5)
            node = [i for i in driver.list_nodes() if i.uuid == node.uuid][0]

        # if we try to connect in ssh without waiting, it says that the key is not valid. Probably it takes time to
        # complete the configuration of the public ip and/or copy of the public key on the vm
        #time.sleep(15)

        vm = VM(node.id, node.public_ips[0], self.vm_user, self.key_path, self.platform, self.working_dir)

        self.__execute_post_create(vm, 5)

        return vm


    def __get_available_public_ip(self, driver):
        public_ips = driver.ex_list_floating_ips()

        if public_ips:
            av = [i for i in public_ips if not i.node_id]
            if av:
                return av[0]
        return None

    def __execute_post_create(self, vm, retries):
        print('Try to connect to the new vm (max_retries={0})'.format(retries))
        try:
            if retries > 0:
                run_ssh_cmd(vm, self.post_create_script, needs_pty=True)
        except:
            time.sleep(10)
            retries -= 1
            self.__execute_post_create(vm,retries)


    @staticmethod
    def load_from_config_file(config: ConfigParser, service_type: str) -> ServiceProvider:

        cp = LibcloudComputeProvider(
            config['provider']['type'],
            config['provider']['endpoint'],
            config['provider']['access_id'],
            config['provider']['secret_key']
        )

        if 'libcloud_extra_params' in config:
            libcloud_additional_params = {}
            for k in config['libcloud_extra_params']:
                libcloud_additional_params[k] = config['libcloud_extra_params'][k]

            cp.extra_params = libcloud_additional_params

        cloud_service_config = config[service_type]

        cp.image = cloud_service_config['image']
        cp.size = cloud_service_config['size']
        cp.key_name = cloud_service_config['key_name']
        cp.key_path = cloud_service_config['key_path']
        cp.vm_user = cloud_service_config['vm_user']
        cp.working_dir = '/home/' + cloud_service_config['vm_user'] # default value
        cp.platform = cloud_service_config['platform']


        if 'working_dir' in cloud_service_config:
            cp.working_dir = cloud_service_config['working_dir']

        if 'post_create_script' in cloud_service_config:
            cp.post_create_script = cloud_service_config['post_create_script']

        return cp
