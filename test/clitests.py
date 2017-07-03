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

from org.benchsuite import cli
from org.benchsuite.controller import CONFIG_FOLDER_VARIABLE_NAME

if __name__ == '__main__':

   os.environ[CONFIG_FOLDER_VARIABLE_NAME] = '/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig'

   # cli.main('new-session --provider filab-vicenza --service ubuntu_large'.split())

   # cli.main('new-exec be3a3fe1-5ffd-11e7-a491-742b62857160 cloudsuite-graphanalytics Workload1'.split())

   cli.main('run-exec 97321c8c-6008-11e7-a491-742b62857160'.split())

    # cli.main('run-exec aaa76e0a-5d7b-11e7-8a4f-9c4e36dc7538'.split())


    # cli.main('destroy-session 0e3932f9-5d79-11e7-8a4f-9c4e36dc7538'.split())