# Benchmarking Suite
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
from benchsuite.core.controller import CONFIG_FOLDER_ENV_VAR_NAME

if __name__ == '__main__':

   os.environ[CONFIG_FOLDER_ENV_VAR_NAME] = '/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig'
   os.environ['BENCHSUITE_SERVICE_TYPE'] = 'ubuntu_small'



   with open('/home/ggiammat/projects/ENG.CloudPerfect/workspace/testing/bsconfig/providers/filab-vicenza.conf') as f:
      t = f.read()

   os.environ['BENCHSUITE_PROVIDER'] = t

   main('shell'.split())
   #main('-vvv multiexec --provider amazon-us-west-1 filebench'.split())

   #main('-vvv new-exec 1cbf3f39-c05a-4bf8-becc-42bc192dc71c idle idle30'.split())

   #main('-vvv list-execs'.split())

   # cli.main('-vvv exec --provider amazon-us-west-1 --service ubuntu_micro --tool ycsb-mongodb --workload WorkloadA'.split())

   #main('prepare-exec 3e5c2c78-a36b-11e7-a0e8-742b62857160'.split())

   #main('-vvv new-exec 9ca3b4ce-f652-4faf-8e48-267f3f4c1460 filebench varmail_short'.split())

   #main('-vvv run-exec 1516f866-88d6-11e7-9f96-742b62857160'.split())