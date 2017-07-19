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

from benchsuite.cli.command import main
from benchsuite.core.config import CONFIG_FOLDER_VARIABLE_NAME

if __name__ == '__main__':

   os.environ[CONFIG_FOLDER_VARIABLE_NAME] = '/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig'

   # cli.main('new-session --provider filab-vicenza --service ubuntu_large'.split())

   # cli.main('new-exec e95a1333-619a-11e7-9084-742b62857160 idle idle30'.split())

   # cli.main('-vvv exec --provider amazon-us-west-1 --service ubuntu_micro --tool ycsb-mongodb --workload WorkloadA'.split())

    # cli.main('run-exec aaa76e0a-5d7b-11e7-8a4f-9c4e36dc7538'.split())


   main('-vvv prepare-exec 0b3275f6-6bcf-11e7-8e0a-742b62857160'.split())