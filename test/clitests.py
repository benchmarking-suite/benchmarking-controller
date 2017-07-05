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

from benchsuite.controller import CONFIG_FOLDER_VARIABLE_NAME

from benchsuite import cli

if __name__ == '__main__':

   os.environ[CONFIG_FOLDER_VARIABLE_NAME] = '/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig'

   # cli.main('new-session --provider filab-vicenza --service ubuntu_large'.split())

   # cli.main('new-exec 145f9d81-6188-11e7-9084-742b62857160 idle idle30'.split())

   # cli.main('-vvv prepare-exec 9cd1aa96-6188-11e7-9084-742b62857160'.split())

    # cli.main('run-exec aaa76e0a-5d7b-11e7-8a4f-9c4e36dc7538'.split())


   cli.main('-vvv list-sessions'.split())